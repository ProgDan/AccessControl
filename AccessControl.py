#!/usr/bin/python3
# -*- coding: utf8 -*-
#
#    Copyright 2018 Daniel Arndt Alves <progdan@gmail.com>
#
#    This file is part of AccessControl
#    AccessControl is a simple Python implementation for
#    the MFRC522 NFC Card Reader and Access Control System 
#    for the Raspberry Pi.
#
#    AccessControl is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AccessControl is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with AccessControl.  If not, see <http://www.gnu.org/licenses/>.
#
# Programa: Rotina principal do controle de acesso
# Ponto de entrada da aplicação

import Adafruit_CharLCD as LCD
import socket
import os
import time
import RPi.GPIO as GPIO
import sqlite3

import RFID.MFRC522

from datetime import datetime

import Buzzer.buzzer as buzzer

############### Settings ####################
# DB Name
DB_NAME = "./DB/access.db"

# Pino Buzzer
myBuzzer = buzzer.buzzer(4)

# Pinos LCD x Raspberry (GPIO)
lcd_rs        = 18
lcd_en        = 23
lcd_d4        = 12
lcd_d5        = 16
lcd_d6        = 20
lcd_d7        = 21
lcd_backlight = 4

# Define numero de colunas e linhas do LCD
lcd_colunas = 16
lcd_linhas  = 2
##############################################

# UID dos cartões que possuem acesso liberado.
CARTOES_LIBERADOS = {
    '72:8:6B:1F:E': 'Master',
    '3C:2F:4F:0:2D': 'Teste',
    'E:3:16:D3:C8': 'Blue 01',
    'E7:5E:16:D3:7C': 'Blue 02',
    '31:DF:92:EF:93': 'Blue 03',
    '59:A5:8B:4C:3B': 'Blue 04',
    'D9:A5:EA:4B:DD': 'Blue 05',
}

# Le as informacoes do endereco IP
gw = os.popen("ip -4 route show default").read().split()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((gw[2], 0))
ipaddr = s.getsockname()[0]

# Inicializa o LCD nos pinos configurados acima
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5,
                           lcd_d6, lcd_d7, lcd_colunas, lcd_linhas,
                           lcd_backlight)

# Functions definitions
def create_connection(db_file):
    """ create a database connection # Program start from here to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
 
    return None

def select_usuario(conn, uid):
    """
    Query usuario by uid
    :param conn: the Connection object
    :param uid:
    :return: UsrCodigo
    """
    cur = conn.cursor()
    cur.execute("SELECT UsrCodigo FROM Usuario WHERE UsrBarra=?", (uid,))
 
    rows = cur.fetchall()
 
    for row in rows:
        return row
    
    return None

def select_UsrNome(conn, UsrCodigo):
    """
    Query UsrNome by UsrCodigo
    :param conn: the Connection object
    :param UsrCodigo:
    :return: UsrNome
    """
    cur = conn.cursor()
    cur.execute("SELECT UsrNome FROM Usuario WHERE UsrCodigo=?", (UsrCodigo,))
 
    rows = cur.fetchall()
 
    for row in rows:
        return row
    
    return None



def gera_movimento(conn, movimento):
    """
    Create a new movimento into the Movimento table
    :param conn:
    :param movimento:
    :return: movimento id
    """
    sql = ''' INSERT INTO Movimento(MovData, MovBarra, MovSentido, MovBloqueado, MovForaHorario, MovProvisorio, UsrCodigo)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, movimento)
    return cur.lastrowid

def setup():
    GPIO.setmode(GPIO.BCM)
    
    lcd.clear()
    
    # Imprime texto na primeira linha
    lcd.set_cursor(3,0)
    lcd.message('CDA CONTROL')
    
    # Mostra o endereco IP na segunda linha
    lcd.message('\nIP %s' %(ipaddr))
    
    # Aguarda 5 segundos
    time.sleep(5.0)
    
    lcd.clear()
    lcd.set_cursor(3,0)
    lcd.message('CDA CONTROL')

def destroy():
    # Release resource
    GPIO.cleanup()
    # Close DB
    conn.close()
    
    print('\nPrograma encerrado.')

# Program start from here
if __name__ == '__main__':
    try:
        setup()
        
        # create a database connection
        conn = create_connection(DB_NAME)
        
        # Inicia o módulo RC522.
        LeitorRFID = RFID.MFRC522.MFRC522()
        
        print('Aproxime seu cartão RFID')

        while True:
            # Verifica se existe uma tag próxima do módulo.
            status, tag_type = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)
            
            if status == LeitorRFID.MI_OK:
                print('Cartão detectado!')
                
                # Efetua leitura do UID do cartão.
                status, uid = LeitorRFID.MFRC522_Anticoll()
                
                if status == LeitorRFID.MI_OK:
                    uid = ':'.join(['%X' % x for x in uid])
                    print('UID do cartão: %s' % uid)
                    
                    # Se o cartão está liberado exibe mensagem de boas vindas.
                    if uid in CARTOES_LIBERADOS:
                        print('Acesso Liberado!')
                        with conn:
                            usuario = select_usuario(conn, uid)
                            usuario_nome = select_UsrNome(conn, usuario[0])
                            movimento = (datetime.now(),uid,'P',0,0,0,int(usuario[0]))
                            gera_movimento(conn, movimento)
                        lcd.clear()
                        lcd.set_cursor(1,0)
                        lcd.message('Acesso Liberado')
                        lcd.set_cursor(0,1)
                        lcd.message(CARTOES_LIBERADOS[uid])
                        myBuzzer.play(myBuzzer.melody_win, myBuzzer.tempo_win, 0.30, 0.800)
                        #print('Olá %s.' % CARTOES_LIBERADOS[uid])
                        print('Olá %s.' % usuario_nome)
                    else:
                        print('Acesso Negado!')
                        with conn:
                            movimento = (datetime.now(),uid,'P',1,0,0,0)
                            gera_movimento(conn, movimento)
                        lcd.set_cursor(1,0)
                        lcd.message('Nao Cadastrado')
                        myBuzzer.play(myBuzzer.melody_fail, myBuzzer.tempo_fail, 0.30, 0.800)
                        
                    print('\nAproxime seu cartão RFID')
                    lcd.clear()
                    lcd.set_cursor(3,0)
                    lcd.message('CDA CONTROL')
            
            lcd.set_cursor(0,1)
            lcd.message(datetime.now().strftime(' %d/%m %H:%M:%S'))
            time.sleep(.25)

        destroy()
    except KeyboardInterrupt:   # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

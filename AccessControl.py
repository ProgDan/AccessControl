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

############### Settings ####################
# DB Name
DB_NAME = "./DB/access.db"

# Pino Buzzer
buzzer_pin = 4

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

# Definicao das Notas Musicais
notes = {
    'B0' : 31,
    'C1' : 33, 'CS1' : 35,
    'D1' : 37, 'DS1' : 39,
    'EB1' : 39,
    'E1' : 41,
    'F1' : 44, 'FS1' : 46,
    'G1' : 49, 'GS1' : 52,
    'A1' : 55, 'AS1' : 58,
    'BB1' : 58,
    'B1' : 62,
    'C2' : 65, 'CS2' : 69,
    'D2' : 73, 'DS2' : 78,
    'EB2' : 78,
    'E2' : 82,
    'F2' : 87, 'FS2' : 93,
    'G2' : 98, 'GS2' : 104,
    'A2' : 110, 'AS2' : 117,
    'BB2' : 123,
    'B2' : 123,
    'C3' : 131, 'CS3' : 139,
    'D3' : 147, 'DS3' : 156,
    'EB3' : 156,
    'E3' : 165,
    'F3' : 175, 'FS3' : 185,
    'G3' : 196, 'GS3' : 208,
    'A3' : 220, 'AS3' : 233,
    'BB3' : 233,
    'B3' : 247,
    'C4' : 262, 'CS4' : 277,
    'D4' : 294, 'DS4' : 311,
    'EB4' : 311,
    'E4' : 330,
    'F4' : 349, 'FS4' : 370,
    'G4' : 392, 'GS4' : 415,
    'A4' : 440, 'AS4' : 466,
    'BB4' : 466,
    'B4' : 494,
    'C5' : 523, 'CS5' : 554,
    'D5' : 587, 'DS5' : 622,
    'EB5' : 622,
    'E5' : 659,
    'F5' : 698, 'FS5' : 740,
    'G5' : 784, 'GS5' : 831,
    'A5' : 880, 'AS5' : 932,
    'BB5' : 932,
    'B5' : 988,
    'C6' : 1047, 'CS6' : 1109,
    'D6' : 1175, 'DS6' : 1245,
    'EB6' : 1245,
    'E6' : 1319,
    'F6' : 1397, 'FS6' : 1480,
    'G6' : 1568, 'GS6' : 1661,
    'A6' : 1760, 'AS6' : 1865,
    'BB6' : 1865,
    'B6' : 1976,
    'C7' : 2093, 'CS7' : 2217,
    'D7' : 2349, 'DS7' : 2489,
    'EB7' : 2489,
    'E7' : 2637,
    'F7' : 2794, 'FS7' : 2960,
    'G7' : 3136, 'GS7' : 3322,
    'A7' : 3520, 'AS7' : 3729,
    'BB7' : 3729,
    'B7' : 3951,
    'C8' : 4186, 'CS8' : 4435,
    'D8' : 4699, 'DS8' : 4978
}

melody = [
  notes['E7'], notes['E7'], 0, notes['E7'],
  notes['E7'], 0, notes['E7'], notes['E7']
]
tempo = [
  12, 12, 12, 12,
  12, 12, 12, 12,
  12
]

melody_win = [
  notes['A5'], notes['B5'], notes['C5'],
  notes['B5'], notes['C5'], notes['D5'],
  notes['C5'], notes['D5'], notes['E5'],
  notes['D5'], notes['E5'], notes['E5']
]
tempo_win = [
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12
]

melody_fail = [
  notes['G4'], notes['C4'], notes['G4'],
  notes['C4'], notes['G4'], notes['C4']
]
tempo_fail = [
  12, 12, 12, 12,
  12, 12
]
# Program start from here
def create_connection(db_file):# Program start from here
    """ create a database connection # Program start from hereto the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
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

def buzz(frequency, length):     #create the function "buzz" and feed it the pitch and duration)

    if(frequency==0):
        time.sleep(length)
        return
    period = 1.0 / frequency         #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
    delayValue = period / 2      #calcuate the time for half of the wave
    numCycles = int(length * frequency)  #the number of waves to produce is the duration times the frequency
    
    for i in range(numCycles):      #start a loop from 0 to the variable "cycles" calculated above
        GPIO.output(buzzer_pin, True)    #set pin 27 to high
        time.sleep(delayValue)      #wait with pin 27 high
        GPIO.output(buzzer_pin, False)      #set pin 27 to low
        time.sleep(delayValue)      #wait with pin 27 low

def play(melody,tempo,pause,pace=0.800):
    
    for i in range(0, len(melody)):     # Play song
        
        noteDuration = pace/tempo[i]
        buzz(melody[i],noteDuration)    # Change the frequency along the song note
        
        pauseBetweenNotes = noteDuration * pause
        time.sleep(pauseBetweenNotes)


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.IN)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    
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

if __name__ == '__main__':      # Program start from here
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
                        play(melody_win, tempo_win, 0.30, 0.800)
                        #print('Olá %s.' % CARTOES_LIBERADOS[uid])
                        print('Olá %s.' % usuario_nome)
                    else:
                        print('Acesso Negado!')
                        with conn:
                            movimento = (datetime.now(),uid,'P',1,0,0,0)
                            gera_movimento(conn, movimento)
                        lcd.set_cursor(1,0)
                        lcd.message('Nao Cadastrado')
                        play(melody_fail, tempo_fail, 0.30, 0.800)
                        
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

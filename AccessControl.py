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

from classes.Connect import Connect as Connect
from classes.UsrDb import UsrDb as UsrDb
from classes.MovDB import MovDb as MovDb
from classes.HorDB import HorDb as HorDb
from classes.usuario import Usuario as Usuario
from classes.movimento import Movimento as Movimento
from classes.horario import Horario as Horario

__author__ = "Daniel Arndt Alves"
__copyright__ = "Daniel Arndt Alves (2019)"
__email__ = "progdan@gmail.com"
__status__ = "Prototype"


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
    db.close_db()
    
    print('\nPrograma encerrado.')

# Program start from here
if __name__ == '__main__':
    try:
        setup()
        
        # create a database connection
        db = Connect(DB_NAME)
        
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

                    # Busca o cartão detectado no banco de dados
                    usuario_db = UsrDb(db)
                    mov_db = MovDb(db)
                    hora_db = HorDb(db)
                    usrcartao = usuario_db.find_user_by_card(uid)
                    if(usrcartao.getUsrCodigo() != 0):
                        if(usrcartao.getUsrProvisorio() == uid):
                            print('Cartao Provisorio!')
                            # Verifica se o cartao provisorio esta vencido
                            if(usrcartao.getUsrProvisorioValidade() < datetime.now().timestamp()):
                                print('Cartao Provisorio Vencido!')
                                mov = Movimento(datetime.now().timestamp(),uid,'P',1,0,1,usrcartao.getUsrCodigo())
                                mov_db.insert_movimento(mov)
                                lcd.set_cursor(1,0)
                                lcd.message('Provis. Vencido')
                                myBuzzer.play(myBuzzer.melody_fail, myBuzzer.tempo_fail, 0.30, 0.800)
                            else:
                                print('Cartao Provisorio Valido!')
                                # Verifica o horario de movimento
                                if(hora_db.check_horario_by_user(usrcartao.getUsrCodigo(), (datetime.today().weekday()+1)%7, datetime.now())):
                                    print('Acesso Liberado!')
                                    mov = Movimento(datetime.now().timestamp(),uid,'P',0,0,1,usrcartao.getUsrCodigo())
                                    mov_db.insert_movimento(mov)
                                    lcd.set_cursor(1,0)
                                    lcd.message('Acesso Liberado')
                                    lcd.set_cursor(0,1)
                                    lcd.message('Prov. Nome')
                                    myBuzzer.play(myBuzzer.melody_win, myBuzzer.tempo_win, 0.30, 0.800)
                                else:
                                    print('Fora de horario!')
                                    mov = Movimento(datetime.now().timestamp(),uid,'P',1,1,1,usrcartao.getUsrCodigo())
                                    mov_db.insert_movimento(mov)
                                    lcd.set_cursor(1,0)
                                    lcd.message('Prov. Fora hor.')
                                    myBuzzer.play(myBuzzer.melody_fail, myBuzzer.tempo_fail, 0.30, 0.800)
                        else:
                            print('Cartao Pessoal!')
                            # Verifica o horario de movimento
                            if(hora_db.check_horario_by_user(usrcartao.getUsrCodigo(), (datetime.today().weekday()+1)%7, datetime.now())):
                                print('Acesso Liberado!')
                                mov = Movimento(datetime.now().timestamp(),uid,'P',0,0,0,usrcartao.getUsrCodigo())
                                mov_db.insert_movimento(mov)
                                lcd.set_cursor(1,0)
                                lcd.message('Acesso Liberado')
                                lcd.set_cursor(0,1)
                                lcd.message('Nome do Usuario')
                                myBuzzer.play(myBuzzer.melody_win, myBuzzer.tempo_win, 0.30, 0.800)
                            else:
                                print('Fora de horario!')
                                mov = Movimento(datetime.now().timestamp(),uid,'P',1,1,0,usrcartao.getUsrCodigo())
                                mov_db.insert_movimento(mov)
                                lcd.set_cursor(1,0)
                                lcd.message('Fora de horario')
                                myBuzzer.play(myBuzzer.melody_fail, myBuzzer.tempo_fail, 0.30, 0.800)
                    else:
                        print('Nao Cadastrado!')
                        mov = Movimento(datetime.now().timestamp(),uid,'P',1,0,0,0)
                        mov_db.insert_movimento(mov)
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

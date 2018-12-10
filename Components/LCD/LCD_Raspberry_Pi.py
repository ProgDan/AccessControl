#!/usr/bin/python3

# Programa: Teste display LCD 16x2 e Raspberry Pi B+
# (mostra Texto e endereco IP)

import Adafruit_CharLCD as LCD
import socket
import os
import time

from datetime import datetime

# Le as informacoes do endereco IP
gw = os.popen("ip -4 route show default").read().split()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((gw[2], 0))
ipaddr = s.getsockname()[0]

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

# Inicializa o LCD nos pinos configurados acima
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5,
                           lcd_d6, lcd_d7, lcd_colunas, lcd_linhas,
                           lcd_backlight)

lcd.clear()

# Imprime texto na primeira linha
lcd.set_cursor(3,0)
lcd.message('CDA CONTROL')

# Mostra o endereco IP na segunda linha
lcd.message('\nIP %s' %(ipaddr))

# Aguarda 10 segundos
time.sleep(10.0)

lcd.clear()
lcd.set_cursor(3,0)
lcd.message('CDA CONTROL')

while True:
    lcd.set_cursor(0,1)
    lcd.message(datetime.now().strftime(' %d/%m %H:%M:%S'))
    time.sleep(0.5)

#!/usr/bin/python3

import Adafruit_CharLCD as LCD
import socket
import os
import time
import RPi.GPIO as GPIO
import RFID.MFRC522

from datetime import datetime

# UID dos cartões que possuem acesso liberado.
CARTOES_LIBERADOS = {
    '72:8:6B:1F:E': 'Master',
    '3C:2F:4F:0:2D': 'Teste',
}


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

def setup():
    GPIO.setmode(GPIO.BCM)

def destroy():
    GPIO.cleanup()
    print('\nPrograma encerrado.')

if __name__ == '__main__':      # Program start from here
    try:
        setup()
        
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
                        print('Olá %s.' % CARTOES_LIBERADOS[uid])
                    else:
                        print('Acesso Negado!')
                        
                    print('\nAproxime seu cartão RFID')
            
            lcd.set_cursor(0,1)
            lcd.message(datetime.now().strftime(' %d/%m %H:%M:%S'))
            time.sleep(.25)

        destroy()
    except KeyboardInterrupt:   # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()

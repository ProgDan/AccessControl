#!/usr/bin/python3
# -*- coding: utf8 -*-

"""
Classe em Python 3.5 para controle das portas GPIO (BCM) do Raspberry Pi versões RPi B+, RPi 2B e RPi 3B.

Credits and License: Created by Erivando Sena, adapted by Daniel Arndt Alves (2019)

 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License.
"""

import os
import yaml
from RFID.gpio import PinosGPIO

__author__ = "Daniel Arndt Alves (Adaptations)"
__copyright__ = "Erivando Sena (2016)"
__email__ = "progdan@gmail.com"
__status__ = "Prototype"

PINOS_YML = os.path.join(os.path.dirname(os.path.abspath(__file__)),"pinos.yml")

class PinoControle(PinosGPIO):
    
    print ("GPIO v." + str(PinosGPIO().gpio.VERSION))

    def __init__(self):
        super(PinoControle, self).__init__()
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setwarnings(False)
        self.carrega_yaml()

    def carrega_yaml(self):
        try:
            with open(PINOS_YML) as file_data:
                self.pins = yaml.safe_load(file_data)
        except Exception as e:
            print(e)

    def pino_response(self, numero, config):
        try:
            output = {
                'nome': config.get('nome'),
                'gpio': numero,
                'modo': config.get('modo'),
                'estado': self.gpio.input(numero)
            }
            resistor = config.get('resistor')
            if resistor:
                output['resistor'] = resistor
            return output
        except Exception as e:
            print(e)
            
    def atualiza(self, numero, valor):
        pino_numero = int(numero)
        try:
            self.pins[pino_numero]
            self.gpio.output(pino_numero, valor)
            estado = self.gpio.input(pino_numero)
            return estado
        except Exception as e:
            print(e)
            
    def estado(self, numero):
        pino_numero = int(numero)
        try:
            estado = self.gpio.input(pino_numero)
            return estado
        except Exception as e:
            print(e)
        
    def ler(self, numero):
        pino_numero = int(numero)
        pino_habilitado = None
        try:
            pino_config = self.pins[pino_numero]
            if pino_config['modo'] == 'OUT':
                self.gpio.setup(pino_config['gpio'], self.gpio.OUT)
                print(pino_config['nome'])
            if pino_config['modo'] == 'IN':
                self.gpio.setup(pino_config['gpio'], self.gpio.IN, pull_up_down= self.gpio.PUD_UP if pino_config['resistor'] == 'PUD_UP' else self.gpio.PUD_DOWN)
                print(pino_config['nome'])
            pino_habilitado = self.pino_response(pino_numero, pino_config)
            return pino_habilitado
        except Exception as e:
            print(e)
			
    def entrada(self):
        return self.gpio.IN

    def saida(self):
        return self.gpio.OUT

    def baixo(self):
        return self.gpio.LOW

    def alto(self):
        return self.gpio.HIGH

    def desativa_avisos(self):
        return self.gpio.setwarnings(False)

    def limpa(self):
        print("GPIO's clean pins!")
        return self.gpio.cleanup()

    def __del__(self):
        self.limpa()
    
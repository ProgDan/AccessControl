#!/usr/bin/python3
# -*- coding: utf8 -*-
"""
Class in Python 3.5 that executes a Thread for reading RFID tags.
Credits and License: Created by Erivando Sena, adapted by Daniel Arndt Alves (2019)

 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License.
"""

import threading
from time import sleep
from RFID.nfc_522 import Nfc522

__author__ = "Daniel Arndt Alves  (Adaptations)"
__copyright__ = "Erivando Sena (2016)"
__email__ = "progdan@gmail.com"
__status__ = "Prototype"


class LeitorCartao(threading.Thread):
    
    nfc = Nfc522()
    numero_cartao = None
    
    def __init__(self, intervalo=0.2):
        threading.Thread.__init__(self)
        self._stopevent = threading.Event()
        self._sleepperiod = intervalo
        self.name = 'Thread LeitorCartao'
        
    def run(self):
        print("%s. Run... " % self.name)
        while not self._stopevent.isSet():
            self.ler()
            self._stopevent.wait(self._sleepperiod)
        print("%s.Turning off..." % (self.getName(),))
        
    def obtem_numero_cartao_rfid(self):
        id = None
        try:
            while True:
                id = self.nfc.obtem_nfc_rfid()
                if id:
                    id = str(id).zfill(10)
                    if (len(id) >= 10):
                        self.numero_cartao = id
                        print("Read TAG Number: " +str(self.numero_cartao))
                        return self.numero_cartao
                    else:
                        print("Error TAG Number: " +str(self.numero_cartao))
                        id = None
                        return None
                else:
                    return id
        except Exception as e:
            print(e)
            
    def ler(self):
        try:
            if self.obtem_numero_cartao_rfid():
                self.valida_cartao(self.numero_cartao)
            else:
                return None
        except Exception as e:
            print(e)
            
    def valida_cartao(self, numero):
        try:
            print("I make interesting operations here with the tag:" + str(numero))
        except Exception as e:
            print(e)

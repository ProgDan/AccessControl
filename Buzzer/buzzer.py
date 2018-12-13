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
# Programa: Rotina de configuração e controle de música para o Buzzer

def notes():
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

def melody():
    # Definição de Melodia e Tempo
    melody = [
    notes['E7'], notes['E7'], 0, notes['E7'],
    notes['E7'], 0, notes['E7'], notes['E7']
    ]

    tempo = [
    12, 12, 12, 12,
    12, 12, 12, 12,
    12
    ]

def melody_win():
    # Definição do buzzer de Acesso Liberado
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

def melody_fail():
    # Definição do buzzer de Acesso Bloqueado
    melody_fail = [
    notes['G4'], notes['C4'], notes['G4'],
    notes['C4'], notes['G4'], notes['C4']
    ]
    tempo_fail = [
    12, 12, 12, 12,
    12, 12
    ]

#!/usr/bin/python3
# -*- coding: utf8 -*-

import time
import RPi.GPIO as GPIO

class Buzzer:
    def __init__(self,buzzer_pin):
        self.buzzer_pin = buzzer_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.buzzer_pin, GPIO.IN)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)

        # Music Notes definition
        self.notes = {
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

        # Default Alarm definition
        self.melody = [
            self.notes['E7'], self.notes['E7'], 0, self.notes['E7'],
            self.notes['E7'], 0, self.notes['E7'], self.notes['E7']
        ]
        self.tempo = [
            12, 12, 12, 12,
            12, 12, 12, 12, 12
        ]

        # Success Alarm definition
        self.melody_win = [
            self.notes['A5'], self.notes['B5'], self.notes['C5'],
            self.notes['B5'], self.notes['C5'], self.notes['D5'],
            self.notes['C5'], self.notes['D5'], self.notes['E5'],
            self.notes['D5'], self.notes['E5'], self.notes['E5']
        ]
        self.tempo_win = [
            12, 12, 12, 12,
            12, 12, 12, 12,
            12, 12, 12, 12,
            12, 12, 12, 12
        ]

        # Fail Alarm definition
        self.melody_fail = [
            self.notes['G4'], self.notes['C4'], self.notes['G4'],
            self.notes['C4'], self.notes['G4'], self.notes['C4']
        ]
        self.tempo_fail = [
            12, 12, 12, 12,
            12, 12
        ]

    # create the function "buzz" and feed it the pitch and duration)
    def buzz(self, frequency, length):

        if(frequency == 0):
            time.sleep(length)
            return
        # in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
        period = 1.0 / frequency
        # calcuate the time for half of the wave
        delayValue = period / 2
        # the number of waves to produce is the duration times the frequency
        numCycles = int(length * frequency)
        
        # start a loop from 0 to the variable "cycles" calculated above
        for i in range(numCycles):
            # set buzzer_pin to high
            GPIO.output(self.buzzer_pin, True)
            # wait with buzzer_pin high
            time.sleep(delayValue)
            # set buzzer_pin to low
            GPIO.output(self.buzzer_pin, False)
            # wait with buzzer_pin low
            time.sleep(delayValue)

    def play(self, melody,tempo,pause,pace=0.800):
        
        # Play song
        for i in range(0, len(melody)):
            
            noteDuration = pace/tempo[i]
            # Change the frequency along the song note
            buzz(melody[i],noteDuration)
            
            pauseBetweenNotes = noteDuration * pause
            time.sleep(pauseBetweenNotes)

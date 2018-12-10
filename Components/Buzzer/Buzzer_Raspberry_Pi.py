#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
#from time import sleep


#Set buzzer - pin 23 as output
Buzzer=4 

CL = [0, 131, 147, 165, 175, 196, 211, 248]     # Frequency of Low C notes
CM = [0, 262, 294, 330, 350, 393, 441, 495]     # Frequency of Middle C notes
CH = [0, 525, 589, 661, 700, 786, 882, 990]     # Frequency of High C notes

song_1 = [  CL[1], CL[2], CL[3], CL[4], CL[5], CL[6], CL[7], # Notes of song1
            CM[1], CM[2], CM[3], CM[4], CM[5], CM[6], CM[7], 
            CL[1], CL[2], CL[3], CL[4], CL[5], CL[6], CL[7], 
            CH[1], CH[2], CH[3], CH[4], CH[6], CH[6], CH[7]    ]

beat_1 = [  1, 1, 1, 1, 1, 1, 1,             # Beats of song 1, 1 means 1/8 beats
            1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1, 
            1, 1, 1, 1, 1, 1, 1  ]

def setup():
    #Disable warnings (optional)
    GPIO.setwarnings(False)
    #Select GPIO mode
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Buzzer, GPIO.OUT)    # Set pins' mode is output
    global Buzz                     # Assign a global variable to replace GPIO.PWM 
    Buzz = GPIO.PWM(Buzzer, 440)    # 440 is initial frequency.
    Buzz.start(50)                  # Start Buzzer pin with 50% duty ration

def loop():
    while True:
        print('\n    Playing song 1...')
        for i in range(1, len(song_1)):     # Play song 1
            Buzz.ChangeFrequency(song_1[i]) # Change the frequency along the song note
            time.sleep(beat_1[i] * 0.1)     # delay a note for beat * 0.5s
        time.sleep(1)                       # Wait a second for next song.

def destory():
    Buzz.stop()                 # Stop the buzzer
    GPIO.output(Buzzer, 1)      # Set Buzzer pin to High
    GPIO.cleanup()              # Release resource

if __name__ == '__main__':      # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:   # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destory()


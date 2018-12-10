#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
#from time import sleep

#Disable warnings (optional)
GPIO.setwarnings(False)

#Select GPIO mode
GPIO.setmode(GPIO.BCM)

#Set buzzer - pin 23 as output
buzzer=4 
GPIO.setup(buzzer,GPIO.OUT)

#Run forever loop
while True:
    GPIO.output(buzzer,GPIO.HIGH)
    print ("Beep")
    #sleep(0.5) # Delay in seconds
    time.sleep(1/1000000.0)
    GPIO.output(buzzer,GPIO.LOW)
    print ("No Beep")
    #sleep(0.5)
    time.sleep(1/1000000.0)

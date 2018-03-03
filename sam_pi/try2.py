#!/usr/bin/python

import led.LED as LED
import RPi.GPIO as GPIO
import thread
import time
import display.LCD as LCD

print("hello")

LCD.init()
led = LED.LED()

try:
    thread.start_new_thread(LCD.displaymessage("Swipe your card to start the practical"), ()) 
    thread.start_new_thread(led.greenled, ())
except:
    print("Error: enable to start thread")
    
while 1:
    pass


GPIO.cleanup()



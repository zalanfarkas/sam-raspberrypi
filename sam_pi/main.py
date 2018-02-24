#!/usr/bin/python

import RPi.GPIO as GPIO
import nfc.nfcread
import display.LCD as LCD
import time

LCD.init()

LCD.write("Welcome")
LCD.nextline()
message = "Swipe your card to start the practical"
LCD.write(message)
for i in range(0,len(message) - 16):
    time.sleep(0.5)
    LCD.shiftleft()
    
print nfcread.readNFC()

GPIO.cleanup()

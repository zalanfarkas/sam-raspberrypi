#!/usr/bin/python

import RPi.GPIO as GPIO
import nfc.nfcread as nfcread
import display.LCD as LCD
import time
import thread

LCD.init()

LCD.write("Welcome")
LCD.nextline()
message = "Swipe your card to start the practical"
LCD.write(message)
for i in range(0,len(message) - 16):
    time.sleep(0.5)
    LCD.shiftleft()


try:
   thread.start_new_thread(nfcread.pollPendingPracticals)
except:
   print "Error: unable to start thread"
   
   
print nfcread.readNFC()

GPIO.cleanup()

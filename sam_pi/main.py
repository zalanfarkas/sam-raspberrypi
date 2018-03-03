#!/usr/bin/python

import RPi.GPIO as GPIO
import nfc.nfcread as nfcread
import display.LCD as LCD
import time
import thread
import led.LED as LED

LCD.init()
led = LED.LED()

try:
   thread.start_new_thread(nfcread.pollPendingPracticals, ())
   thread.start_new_thread(nfcread.readNFC, ())
except:
   print "Error: unable to start thread"
   
while 1:
    pass

GPIO.cleanup()

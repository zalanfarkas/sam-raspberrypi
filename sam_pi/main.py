#!/usr/bin/python

import RPi.GPIO as GPIO
import nfc.nfcread as nfcread
import display.LCD as LCD
<<<<<<< HEAD

LCD.init()
  
nfcread.readNFC()
=======
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
>>>>>>> 3a0a74588b7b43cea3a0fb75b7126350066f0b8e

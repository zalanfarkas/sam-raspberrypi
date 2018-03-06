#!/usr/bin/python

import nfc.nfcread as nfcread
import RPi.GPIO as GPIO
import lcd.LCD as LCD
import led.LED as LED
import thread
import time


def main():
   LCD.init()
   LED.init()

   try:
      thread.start_new_thread(nfcread.pollPendingPracticals, ())
      thread.start_new_thread(nfcread.readNFC, ())
   except:
      print "Error: unable to start thread"
      
   while 1:
       pass

   GPIO.cleanup()


if __name__ == '__main__':
   main()

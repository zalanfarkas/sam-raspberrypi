#!/usr/bin/python


from fingerprint.Fingerprint import Fingerprint
from network.Parser import Parser
from network.Poller import Poller
import nfc.nfcread as nfcread
import RPi.GPIO as GPIO
import lcd.LCD as LCD
import led.LED as LED
import thread
import time

def main():
   LCD.init()
   LED.init()
   parser = Parser()
   fingerprint = Fingerprint()
   poller = Poller(parser, fingerprint, 1)
   
   try:
      #thread.start_new_thread(nfcread.pollPendingPracticals, (parser,))
      thread.start_new_thread(nfcread.readNFC, (parser, fingerprint,))
      thread.start_new_thread(poller.startPolling, ())
   except:
      print "Error: unable to start thread"
      
   while True:
       fingerprint.start(parser)

   GPIO.cleanup()


if __name__ == '__main__':
   main()

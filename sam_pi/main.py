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
import threading

import os

def main():
   LCD.init()
   LED.init()
   parser = Parser()
   fingerprint = Fingerprint()
   #poller = Poller(parser, fingerprint, 1)

   # Create child process
   pid = os.fork()

   # Parent process
   if pid:
      try:
         threading.Thread(target=LCD.start).start()
         threading.Thread(target=nfcread.readNFC, args=(parser, fingerprint,)).start()
         #threading.Thread(target=poller.startPolling).start()
         #thread.start_new_thread(LCD.start, ())
         #thread.start_new_thread(nfcread.pollPendingPracticals, (parser,))
         #thread.start_new_thread(nfcread.readNFC, (parser, fingerprint,))
         #thread.start_new_thread(poller.startPolling, ())
      except:
         print "Error: unable to start thread"
   else:
      fingerprint.start(parser)
   #threading.Thread(target=fingerprint.start, args=(parser,)).start()
   #print(threading.active_count())
   #fingerprint.start(parser)

      #time.sleep(5)
      #pass

if __name__ == '__main__':
   main()

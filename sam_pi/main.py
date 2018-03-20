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
import sys
import signal
import os
from multiprocessing import Pipe

def main():
   #Create unix pipe
   main_pipe, fingerpint_pipe = Pipe()
   LCD_IN, LCD_OUT = Pipe()
   
   LCD.init()
   LED.init()
   parser = Parser()
   poller = Poller(parser, fingerpint_pipe, 1)
   # Create child process
   pid = os.fork()

   # Parent process
   if pid:
      try:
         lcd_thread = threading.Thread(target=LCD.new_start, args=(LCD_IN,))
         lcd_thread.daeomon = True
         lcd_thread.start()
         nfc_thread = threading.Thread(target=nfcread.readNFC, args=(parser, fingerpint_pipe, LCD_OUT,))
         nfc_thread.daeomon = True
         nfc_thread.start()
         poll_thread = threading.Thread(target=poller.startPolling)
         poll_thread.daeomon = True
         poll_thread.start()
         #threading.Thread(target=LCD.new_start, args=(LCD_IN,)).start()
         #threading.Thread(target=nfcread.readNFC, args=(parser, fingerpint_pipe, LCD_OUT,)).start()
         #threading.Thread(target=poller.startPolling).start()


         #thread.start_new_thread(LCD.new_start, (LCD_IN,))
         #thread.start_new_thread(nfcread.readNFC, (parser, fingerpint_pipe, LCD_OUT,))
         #thread.start_new_thread(poller.startPolling, ())

         #thread.start_new_thread(LCD.start, ())
         #thread.start_new_thread(nfcread.pollPendingPracticals, (parser,))
         #thread.start_new_thread(nfcread.readNFC, (parser, fingerprint,))
         #thread.start_new_thread(poller.startPolling, ())
      except:
         print "Error: unable to start thread"
      try:
         while 1:
            if fingerpint_pipe.poll(1):
               parser.course_id = fingerpint_pipe.recv()
      except KeyboardInterrupt:
         os.kill(pid, signal.SIGKILL)
         os.kill(os.getpid(), signal.SIGKILL)
         sys.exit()
         
         
   else:
      try:
      #thread.start_new_thread(LCD.new_start, (LCD_IN,))
      #threading.Thread(target=LCD.start).start()
         fingerprint = Fingerprint()
         fingerprint.start(parser, main_pipe, LCD_OUT)
      except KeyboardInterrupt:
         sys.exit()

if __name__ == '__main__':
   main()

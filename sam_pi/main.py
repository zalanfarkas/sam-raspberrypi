#!/usr/bin/python
# Copyright (c) 2018 Team Foxtrot
# Licensed under MIT License

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
   
   # Initializes LCD and LED
   LCD.init()
   LED.init()
   # Create an object of the class Parser and Poller
   parser = Parser()
   poller = Poller(parser, fingerpint_pipe, 1)
   # Create child process
   pid = os.fork()

   # Parent process
   if pid:
      try:
         # start the individual threads for LCD, NFC and poller
         lcd_thread = threading.Thread(target=LCD.new_start, args=(LCD_IN,))
         lcd_thread.daeomon = True
         lcd_thread.start()
         nfc_thread = threading.Thread(target=nfcread.readNFC, args=(parser, fingerpint_pipe, LCD_OUT,))
         nfc_thread.daeomon = True
         nfc_thread.start()
         poll_thread = threading.Thread(target=poller.startPolling)
         poll_thread.daeomon = True
         poll_thread.start()
      except:
         print "Error: unable to start thread"
      try:
         # Poll fingerprint pipe
         while 1:
            if fingerpint_pipe.poll(1):
               parser.course_id = fingerpint_pipe.recv()
      # Kill the threads and clears the LCD screen
      except KeyboardInterrupt:
         LCD.clear()
         os.kill(pid, signal.SIGKILL)
         os.kill(os.getpid(), signal.SIGKILL)
         sys.exit()
         
         
   else:
      # Start fingerprint on child procces
      try:
         fingerprint = Fingerprint()
         fingerprint.start(parser, main_pipe, LCD_OUT)
      # Clear the screen
      except KeyboardInterrupt:
         LCD.clear()
         sys.exit()

# run the main file
if __name__ == '__main__':
   main()

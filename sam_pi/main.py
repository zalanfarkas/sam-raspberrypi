#!/usr/bin/python

import RPi.GPIO as GPIO
import nfc.nfcread as nfcread
import display.LCD as LCD

LCD.init()
  
nfcread.readNFC()

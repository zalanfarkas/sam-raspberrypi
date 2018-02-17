#!/usr/bin/python

import nfcread
import RPi.GPIO as GPIO
#import display

#display.init()

# Welcome message
#display.lcdWriteFirstLine("Welcome")
#display.lcdWriteSecondLine("Swipe your card")

print nfcread.readNFC()

GPIO.cleanup()

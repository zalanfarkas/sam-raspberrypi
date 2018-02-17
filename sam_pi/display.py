#!/usr/bin/python

import RPi.GPIO as GPIO
import time
#import logging

# Define GPIO to LCD mapping
LCD_RS = 22 # Register select (select command mode - 0, or data mode - 1)
LCD_EN = 17 # Enabled
# Only 4 bit operations will be used, so only 4 highest data pins will be used
LCD_D4 = 23
LCD_D5 = 24
LCD_D6 = 4
LCD_D7 = 18

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

def init():
  GPIO.setmode(GPIO.BOARD)     # Use BCM BOARD numbers
  GPIO.setup(LCD_EN, GPIO.OUT) # EN
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  # Initialise display
  lcdWriteByte(0x33,LCD_CMD)
  lcdWriteByte(0x32,LCD_CMD)
  lcdWriteByte(0x28,LCD_CMD)
  lcdWriteByte(0x0C,LCD_CMD)
  lcdWriteByte(0x06,LCD_CMD)
  lcdWriteByte(0x01,LCD_CMD)
  #logging.info("Display initialized")

def lcdWriteFirstLine(text):
    lcdWriteByte(LCD_LINE_1, LCD_CMD)
    lcdWriteString(text)

def lcdWriteSecondLine(text):
    lcdWriteByte(LCD_LINE_2, LCD_CMD)
    lcdWriteString(text)

def lcdWriteString(message):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcdWriteByte(ord(message[i]),LCD_CHR)

def lcdWriteByte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

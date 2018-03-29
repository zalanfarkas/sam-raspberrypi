# Copyright (c) 2018 Team Foxtrot
# Licensed under MIT License

import RPi.GPIO as GPIO
import time
from threading import Thread

# GPIO stands for general general-purpose input/output
RED = 40 # GPIO Pin #40
GREEN = 38 # GPIO Pin #38

# Initializes GPIO for communication with LEDs
def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RED, GPIO.OUT)
    GPIO.setup(GREEN, GPIO.OUT)

# turns Red LED on and off with 2 sec delay in-between
def redled():
    GPIO.output(RED,True)
    time.sleep(2)
    GPIO.output(RED,False)

# turns Green LED on and off with 2 sec dealay in-between
def greenled():
    GPIO.output(GREEN,True)
    time.sleep(2)
    GPIO.output(GREEN,False)

# creates new thread for Green LED
def asyncGreen():
    g = Thread(target=greenled)
    g.start()

# creates new thread for Red LED
def asyncRed():
    r = Thread(target=redled)
    r.start()

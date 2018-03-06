import RPi.GPIO as GPIO
import time
from threading import Thread

RED = 40
GREEN = 38

def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RED, GPIO.OUT)
    GPIO.setup(GREEN, GPIO.OUT)

def redled():
    GPIO.output(RED,True)
    time.sleep(2)
    GPIO.output(RED,False)

def greenled():   
    GPIO.output(GREEN,True)
    time.sleep(2)
    GPIO.output(GREEN,False)

def asyncGreen():
    g = Thread(target=greenled)
    g.start()

def asyncRed():
    r = Thread(target=redled)
    r.start()

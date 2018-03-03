import RPi.GPIO as GPIO

RED = 40
GREEN = 38

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RED, GPIO.OUT)
    GPIO.setup(GREEN, GPIO.OUT)

def redon():
    GPIO.output(RED,True)

def redoff():
    GPIO.output(RED,False)

def greenon():
    GPIO.output(GREEN,True)

def greenoff():
    GPIO.output(GREEN,False)

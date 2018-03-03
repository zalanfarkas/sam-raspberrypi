import RPi.GPIO as GPIO
import time

class LED:
    RED = 40
    GREEN = 38

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.RED, GPIO.OUT)
        GPIO.setup(self.GREEN, GPIO.OUT)

    def redled(self):
        GPIO.output(self.RED,True)
        time.sleep(5)
        GPIO.output(self.RED,False)

    def greenled(self):
        GPIO.output(self.GREEN,True)
        time.sleep(5)
        GPIO.output(self.GREEN,False)

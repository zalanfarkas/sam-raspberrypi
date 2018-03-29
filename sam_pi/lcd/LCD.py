# Copyright (c) 2018 Team Foxtrot
# Licensed under MIT License

# Partly based on library created by LiquidCrystal Arduino

from threading import Thread
import RPi.GPIO as GPIO
import time

# GPIO stands for general general-purpose input/output
_displayfunction = 0
_displaycontrol = 0
_row_offsets = [None]*4

LCD_RS = 15 # GPIO Pin #15
LCD_EN = 13 # GPIO Pin #13
LCD_DATA = [11,7,5,3] # GPIO Pin #11,7,5,3

LCD_COLS = 16 # Sets the number of columns
LCD_ROWS = 2 # Sets the number of rows

# Initializes GPIO for communication with LCD and calls begin method
def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LCD_RS, GPIO.OUT)
	GPIO.setup(LCD_EN, GPIO.OUT)

	begin()

# Initializes the LCD
def begin():
	global _displayfunction

    _displayfunction |= 0x08

	setRowOffsets(0x00, 0x40, 0x00 + LCD_COLS, 0x40 + LCD_COLS)

	time.sleep(0.05)
	GPIO.output(LCD_RS, 0)
	GPIO.output(LCD_EN, 0)

	write4bits(0x03)
	time.sleep(0.0041)
	write4bits(0x03)
	time.sleep(0.0041)
	write4bits(0x03)
	time.sleep(0.00015)
	write4bits(0x02)

	command(0x20 | _displayfunction)

	_displaycontrol = 0x04 | 0x00 | 0x00
	display()

	clear()

	_displaymode = 0x02 | 0x00
	command(0x04 | _displaymode)

def setRowOffsets(row0,row1,row2,row3):
	_row_offsets[0] = row0;
	_row_offsets[1] = row1;
	_row_offsets[2] = row2;
	_row_offsets[3] = row3;

# Clears the screen
def clear():
	command(1)
	time.sleep(0.002)

def home():
	command(2)
	time.sleep(0.002)

# Shifts the screen to the right
def shiftright():
        command(0x10 | 0x08 | 0x04)
        time.sleep(0.002)

# Shifts the screen to the left
def shiftleft():
        command(0x10 | 0x08 | 0x00)
        time.sleep(0.002)

# Moves to the next row of the screen
def nextline():
	command(192)
	time.sleep(0.002)

# Moves cursor to the right
def moveright():
        command(20)
        time.sleep(0.002)

# Moves cursor to the left
def moveleft():
        command(16)
        time.sleep(0.002)

def display():
	global _displaycontrol

	_displaycontrol |= 0x04
	command(0x08 | _displaycontrol)

def command(value):
	send(value, 0)

# Writes a message to the screen
def write(value):
        clear()
	char = list(value)
	for i in range (0, len(char)):
		send(ord(char[i]), 1)

# Sends the data value to the LCD_RS port
def send(value, mode):
	global LCD_RS
	GPIO.output(LCD_RS, mode)
	write4bits(value >> 4)
	write4bits(value)

# Sends the data value to the LCD_EN port
def pulseEnable():
	GPIO.output(LCD_EN, 0)

	time.sleep(0.000001)
	GPIO.output(LCD_EN, 1)
	time.sleep(0.000001)
	GPIO.output(LCD_EN, 0)
	time.sleep(0.0001)

# Writes a 4bits message
def write4bits(value):
	for i in range(0,4):
		GPIO.setup(LCD_DATA[i], GPIO.OUT)
		GPIO.output(LCD_DATA[i], (value >> i) & 0x01)

	pulseEnable()

# LCD loop which check for new messages
cache = ""
message = ""
wait = False
def new_start(LCD_pipe):
        global cache
        while 1:
                if LCD_pipe.poll():
                        newMessage = LCD_pipe.recv()
                        if newMessage == cache:
                                continue
                        print("Writting message" + newMessage)
                        cache = newMessage
                        write(newMessage)
                        time.sleep(1)

# Creates new thread when message is being written
messagecopy = ""
def asyncWrite(message):
        global messagecopy
        if messagecopy == message:
                return
        else:
                messagecopy = message
                w = Thread(target=write, args=(message,))
                w.start()


# Writes a message on a screen
def displaymessage(message):
        clear()
        # If the message is longer than 16 characters then move the shift the
        # left so the message becomes visible
        if len(message) > 16:
                write(message)
                time.sleep(0.2)
                for i in range(0, len(message) - 16):
                        time.sleep(0.2)
                        shiftleft()
        # If not, then display normally
        else:
                time.sleep(0.2)
                write(message)
        time.sleep(0.1)

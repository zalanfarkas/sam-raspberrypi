import RPi.GPIO as GPIO
import time

_displayfunction = 0
_displaycontrol = 0
_row_offsets = [None]*4

LCD_RS = 15
LCD_EN = 11
LCD_DATA = [16,18,7,12]

LCD_COLS = 16
LCD_ROWS = 2

def init():
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)  
	GPIO.setup(LCD_RS, GPIO.OUT)
	GPIO.setup(LCD_EN, GPIO.OUT)
	
	begin()

def begin():
	global _displayfunction
	#, _numlines, _displacontrol, _displaymode
 
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
  
def clear():
	command(1)
	time.sleep(0.002)
  
def home():
	command(2)
	time.sleep(0.002)
	
def shiftright():
        command(0x10 | 0x08 | 0x04)
        time.sleep(0.002)
        
def shiftleft():
        command(0x10 | 0x08 | 0x00)
        time.sleep(0.002)
  
def nextline():
	command(192)
	time.sleep(0.002)

def moveright():
        command(20)
        time.sleep(0.002)
       
def moveleft():
        command(16)
        time.sleep(0.002)
 
def display():
	global _displaycontrol

	_displaycontrol |= 0x04
	command(0x08 | _displaycontrol)
 
def command(value):
	send(value, 0)

def write(value):
	char = list(value)
	for i in range (0, len(char)):
		send(ord(char[i]), 1)
  
def send(value, mode):
	global LCD_RS
	GPIO.output(LCD_RS, mode)
	write4bits(value >> 4)
	write4bits(value)
  
def pulseEnable():
	GPIO.output(LCD_EN, 0)
	time.sleep(0.000001)
	GPIO.output(LCD_EN, 1)
	time.sleep(0.000001)
	GPIO.output(LCD_EN, 0)
	time.sleep(0.0001)
 
def write4bits(value):
	for i in range(0,4):
		GPIO.setup(LCD_DATA[i], GPIO.OUT)
		GPIO.output(LCD_DATA[i], (value >> i) & 0x01)
			
	pulseEnable()
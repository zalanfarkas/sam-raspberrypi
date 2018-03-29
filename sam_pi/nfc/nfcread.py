#!/usr/bin/env python
# -*- coding: utf8 -*-

from network.Parser import Parser
from nfc.MFRC522 import MFRC522
from threading import Thread
import led.LED as LED
#import lcd.LCD as LCD
import time
import threading

#_____________________________Messages_____________________________#
message1 = " SWIPE CARD TO                          START PRACTICAL"
message2 = "RECORD THE                              ATTANDANCE..."
#message3 = "CARD DETECTED"

def readNFC(parser, fingerprint_pipe, LCD_pipe):
    # Create an object of the class MFRC522
    MIFAREReader = MFRC522()
    # This loop keeps checking for chips. If one is near it will get the UID
    while True:
        # Message for recording attandance
        if parser.course_id == None:
            LCD_pipe.send(" SWIPE CARD TO                          START PRACTICAL")
        else:
            LCD_pipe.send("RECORD THE                              ATTENDANCE...")
            
        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        if parser.end_time != None and parser.end_time < time.localtime():
            parser.course_id = None
          
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            #in_progress = True
            
            #LED.asyncGreen()
            
            print("CARD DETECTED")
            # UID saved as nfcData
            nfc_data = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])
            print(nfc_data)
            if parser.course_id == None:
                course_information = parser.get_course("nfc", nfc_data)
                if course_information.error == None:
                    fingerprint_pipe.send(course_information.course_id)
                    LED.asyncGreen()
                    print("started practical")
                    LCD_pipe.send("COURSE ID " + course_information.course_id + "                        INITIALIZED")
                    if course_information.templates != None:
                        fingerprint_pipe.send(course_information.templates)
                else:
                    LED.asyncRed()
                    LCD_pipe.send(course_information.error)
                    print(course_information.error)

            else:
                attendance_information = parser.record_attendance("nfc", nfc_data)
                if attendance_information.error == None:
                    LED.asyncGreen()
                    LCD_pipe.send("ID: " + attendance_information.student_id + "                             RECORDED")
         
                    #print("Attendance recorded successfully for student with id: " + attendance_information.student_id + "\n")
                else:
                    LED.asyncRed()
                    LCD_pipe.send(attendance_information.error)
                    print("could record attendace")
                    #print("Attendance wasn't recorded succesfully here is the error: " + attendance_information.error + "\n")

        time.sleep(1)

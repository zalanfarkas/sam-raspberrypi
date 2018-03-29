#!/usr/bin/env python
# -*- coding: utf8 -*-
# Copyright (c) 2018 Team Foxtrot
# Licensed under MIT License

from network.Parser import Parser
from nfc.MFRC522 import MFRC522
from threading import Thread
import led.LED as LED
import time
import threading

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
            
            print("CARD DETECTED")
            # UID saved as nfcData
            nfc_data = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])
            print(nfc_data)
            if parser.course_id == None:
                course_information = parser.get_course("nfc", nfc_data)
                # If no error has occured, turn on Green LED and write on LCD
                if course_information.error == None:
                    fingerprint_pipe.send(course_information.course_id)
                    LED.asyncGreen()
                    print("started practical")
                    LCD_pipe.send("COURSE ID " + course_information.course_id + "                        INITIALIZED")
                    if course_information.templates != None:
                        fingerprint_pipe.send(course_information.templates)
                # turn on Red LED and writte error message on LCD
                else:
                    LED.asyncRed()
                    LCD_pipe.send(course_information.error)
                    print(course_information.error)

            else:
                attendance_information = parser.record_attendance("nfc", nfc_data)
                # If no error has occured, turn on Green LED and write on LCD
                if attendance_information.error == None:
                    LED.asyncGreen()
                    LCD_pipe.send("ID: " + attendance_information.student_id + "                             RECORDED")
                # turn on Red LED and write error message on LCD
                else:
                    LED.asyncRed()
                    LCD_pipe.send(attendance_information.error)
                    print("could record attendace")
                    
        # sleep for 1 second before reading the card again
        time.sleep(1)

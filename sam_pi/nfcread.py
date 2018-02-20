#!/usr/bin/env python
# -*- coding: utf8 -*-
import time
import MFRC522
from network.Parser import Parser

def readNFC():
    reading = True
    end_time = None
    parser = Parser()
    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # This loop keeps checking for chips. If one is near it will get the UID
    while reading:
        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()


        if end_time != None and end_time < time.localtime():
            parser.course_id = None
          
        
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # UID saved as nfcData
            nfc_data = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])
            
            if parser.course_id == None:
                course_information = parser.get_course("nfc", nfc_data)
                if course_information.error == None:
                    print("Current course id " + course_information.course_id + " it ends at " + course_information.end_time + "\n")
                    end_time = course_information.end_time
                    # Todo add timeout on end time i.e change course id to none after certain time
                else:
                    print(course_information.error + "\n")
            else:
                attendance_information = parser.record_attendance("nfc", nfc_data)
                if attendance_information.error == None:
                    print("Attendance recorded successfully for student with id: " + attendance_information.student_id + "\n")
                else:
                    print("Attendance wasn't recorded succesfully here is the error: " + attendance_information.error + "\n")
                
            
    
        
'''


    while reading:
        MIFAREReader = MFRC522.MFRC522()

        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        (status,backData) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            print("Card detected")
            MIFAREReader.AntennaOff()
            reading=False
            return str(backData[0])+str(backData[1])+str(backData[2])+str(backData[3])+str(backData[4])
'''

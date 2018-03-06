#!/usr/bin/env python
# -*- coding: utf8 -*-

from network.Parser import Parser
from nfc.MFRC522 import MFRC522
from threading import Thread
import led.LED as LED
import lcd.LCD as LCD
import time

#_____________________________Messages_____________________________#
message1 = " SWIPE CARD TO                          START PRACTICAL"
message2 = "RECORD THE                              ATTANDANCE..."
message3 = "CARD DETECTED"

# Just for test purpose later change to better solution
pi_id = 1

reading = True
end_time = None
parser = Parser()

def pollPendingPracticals():
    while 1:
        global parser, end_time, reading
        print("polling")
        if parser.course_id == None:
            pending_practical = parser.query_pending_practicals(pi_id)
            if pending_practical.error != None:
                print("There was an error:" + pending_practical.error)
            elif pending_practical.pending:
                print("Practical for course: " + pending_practical.course_id + " started")
        time.sleep(20)
    

def readNFC():
    global parser, end_time, reading

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522()

    # This loop keeps checking for chips. If one is near it will get the UID
    while reading:

        # Message for recording attandance
        if parser.course_id == None:
            LCD.asyncWrite(message1)
        else:
            LCD.asyncWrite(message2)
        
        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        if end_time != None and end_time < time.localtime():
            parser.course_id = None
          
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            #in_progress = True
            
            #LED.asyncGreen()
            LCD.asyncWrite(message3)
           
            # UID saved as nfcData
            nfc_data = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])
            
            if parser.course_id == None:
                course_information = parser.get_course("nfc", nfc_data)
                if course_information.error == None:
                    LED.asyncGreen()
                    LCD.asyncWrite("COURSE ID " + course_information.course_id + "                        INITIALIZED")
                    #print("Current course id " + course_information.course_id + " it ends at " + course_information.end_time + "\n")
                    end_time = course_information.end_time
                    # Todo add timeout on end time i.e change course id to none after certain time

                else:
                    LED.asyncRed()
                    LCD.write(course_information.error)
                    #print(course_information.error + "\n")

            else:
                attendance_information = parser.record_attendance("nfc", nfc_data)
                if attendance_information.error == None:
                    LED.asyncGreen()
                    LCD.asyncWrite(attendance_information.student_id)
                    #print("Attendance recorded successfully for student with id: " + attendance_information.student_id + "\n")

                else:
                    LED.asyncRed()
                    LCD.asyncWrite(attendance_information.error)
                    #print("Attendance wasn't recorded succesfully here is the error: " + attendance_information.error + "\n")
        time.sleep(1)       

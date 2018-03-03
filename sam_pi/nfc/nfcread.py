#!/usr/bin/env python
# -*- coding: utf8 -*-

import time
import MFRC522
from network.Parser import Parser
import display.LCD as LCD
import led.LED as LED

# Just for test purpose later change to better solution
pi_id = 1

reading = True
end_time = None
parser = Parser()
LED = LED.LED()


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
    
    LCD.displaymessage("Welcome")
    LCD.displaymessage("Swipe your card to start the practical")
 
    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # This loop keeps checking for chips. If one is near it will get the UID
    while reading:
        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)


        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()


        if end_time != None and end_time < time.localtime():
            parser.course_id = None
          
        
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            LCD.displaymessage("Card detected")
            #LED.greenon()
            # UID saved as nfcData
            nfc_data = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])
            
            if parser.course_id == None:
                course_information = parser.get_course("nfc", nfc_data)
                if course_information.error == None:
                    LCD.displaymessage("Current course id " + course_information.course_id + " it ends at " + course_information.end_time + "\n")
                    #print("Current course id " + course_information.course_id + " it ends at " + course_information.end_time + "\n")
                    end_time = course_information.end_time
                    # Todo add timeout on end time i.e change course id to none after certain time
                else:
                    LCD.displaymessage(course_information.error + "\n")
                    #print(course_information.error + "\n")
            else:
                attendance_information = parser.record_attendance("nfc", nfc_data)
                if attendance_information.error == None:
                    LCD.displaymessage("Attendance recorded successfully for student with id: " + attendance_information.student_id + "\n")
                    #print("Attendance recorded successfully for student with id: " + attendance_information.student_id + "\n")
                else:
                    LCD.displaymessage("Attendance wasn't recorded succesfully here is the error: " + attendance_information.error + "\n")
                    #print("Attendance wasn't recorded succesfully here is the error: " + attendance_information.error + "\n")
                

#!/usr/bin/env python
# -*- coding: utf8 -*-

import MFRC522
from network.Parser import Parser

def readNFC():
    reading = True
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

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # UID saved as nfcData
            nfcData = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])
            parser = Parser("nfc", nfcData)
            course_information = parser.get_course()

            
            if course_information.error == None:
                print("Current course id" + course_information.course_id + " it ends at " + course_information.end_time)
            else:
                print(course_information.error)
                
            MIFAREReader.AntennaOff()
            reading = False

            return nfcData
        
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

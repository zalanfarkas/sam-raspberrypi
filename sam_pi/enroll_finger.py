# Copyright (c) 2018 Team Foxtrot
# Licensed under MIT License

import nfc.MFRC522 as MFRC522
from network.Parser import Parser
from fingerprint.Fingerprint import Fingerprint
import lcd.LCD as LCD
import time

# Create parser
parser = Parser()
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
finerprint_scanner = Fingerprint()
print("Scan your card to identify yourself")

LCD.init()


while(True):
    LCD.write("SCAN CARD")
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        # UID saved as nfcData
        nfc_data = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])
        print("Card                               Detected")
        LCD.write("CARD DETECTED")
        time.sleep(1)
        LCD.write("SCAN FINGER")
        fingerprint = finerprint_scanner.get_template()
        print(fingerprint)
        
        print("Fingeprint data collected")
        LCD.write("DATA COLLECTED")

        result = parser.upload_fingerprint(nfc_data, fingerprint)
        if result.success:
            time.sleep(1)
            LCD.write("SUCCESS")
            print("Template was successfully uploaded")
        else:
            LCD.write("FAILED")
            print("Failed to upload template. Here is the error message: " + result.error)
        print("Scan your card to identify yourself")
        time.sleep(1)

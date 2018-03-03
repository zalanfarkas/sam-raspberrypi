import MFRC522
from network.Parser import Parser
from fingerprint.Fingerprint import Fingerprint

# Create parser
parser = Parser()
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
finerprint_scanner = Fingerprint()

in_progress = False

print("Scan your card to identify yourself")
while(True):
    
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        # UID saved as nfcData
        nfc_data = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])
        print("Card Detected")
        fingerprint = finerprint_scanner.get_template()
        print("Fingeprint data collected")
        result = parser.upload_fingerprint(nfc_data, fingerprint)
        if result.success:
            print("Template was successfully uploaded")
        else:
            print("Failed to upload template. Here is the error message: " + result.error)
        

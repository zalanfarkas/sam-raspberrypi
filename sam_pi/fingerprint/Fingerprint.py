from pyfingerprint.pyfingerprint import PyFingerprint
import lcd.LCD as LCD
import led.LED as LED
import time

class Fingerprint:

    fingerprint = None
    loading_templates = False
    
    def __init__(self):
        try:
            self.fingerprint = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
            if (self.fingerprint.verifyPassword() == False):
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)
            
    def start(self, parser):
        while True:
            # Sleep thread, otherwise pi will get overloaded
            time.sleep(1)
            # Only try to scan fingers, when sensor is not busy
            if self.loading_templates == False:
                # Try to get finger characteristics
                characteristics = self.get_characteristics()
                if characteristics != None:
                    # If course is not started try to start it
                    # otherwise try to record attendance
                    if parser.course_id != None:
                        course_information = parser.get_course("nfc", characteristics)
                        if course_information.error == None:
                            LED.asyncGreen()
                            LCD.asyncWrite("COURSE ID " + course_information.course_id + "                        INITIALIZED")
                        else:
                            LED.asyncRed()
                            LCD.write(course_information.error)
                    else:
                        response = self.parser.record_attendance("fingerprint", characteristics)
                        if response.error == None:
                            LED.asyncGreen()
                            LCD.asyncWrite("Attendance recorded successfully for student with id " + response.student_id)
                        else:
                            LED.asyncRed()
                            LCD.asyncWrite("Error: " + response.error)
    
    def load_templates(self, templates):
        print("Preparing to load templates, current count is: " + str(self.fingerprint.getTemplateCount()))
        # Before loading templates remove old ones
        self.fingerprint.clearDatabase()
        print("Deleted old templates, current count is: " + str(self.fingerprint.getTemplateCount()))
        
        normalized_templates = []
        # Transfer each template from string to array of ints
        for template in course_information.templates:
            normalized_templates.append(map(int, template.split("|")))

        for template in normalized_templates:
            # Load template data to first buffer
            self.fingerprint.uploadCharacteristics(0x01, template)
            # By default code will find free space and store template from first buffer
            # to fingerprint
            self.fingerprint.storeTemplate()
        print("Finished loading templates current count is: "+ str(self.fingerprint.getTemplateCount()))
    
    # Generate template for user
    def get_template(self):
        # Wait for finger
        print('Waiting for finger...')
        while (self.fingerprint.readImage() == False):
            pass

        # Converts image to characteristic and store it to charbuffer 1
        self.fingerprint.convertImage(0x01)
        # Retrieves template characteristics as a 512 bytes array
        template = self.fingerprint.downloadCharacteristics(0x01)
        # Return template as joined string
        return '|'.join(map(str,template))
    
    # Get characteristics
    def get_characteristics(self):
        # Wait that finger is read
        if (self.fingerprint.readImage() == False):
            return

        # Converts read image to characteristics and stores it in charbuffer 1
        self.fingerprint.convertImage(0x01)

        # Searchs template
        result = self.fingerprint.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]
        
        # No match is found
        if (positionNumber == -1):
            LED.asyncRed()
            LCD.asyncWrite("Fingerprint not found")
            return None
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
            print('Waiting for finger...')
        
        # Loads the found template to charbuffer 1
        self.fingerprint.loadTemplate(positionNumber, 0x01)
        # Downloads the characteristics of template loaded in charbuffer 1
        template = self.fingerprint.downloadCharacteristics(0x01)
        # Return template as joined string
        return '|'.join(map(str,template))

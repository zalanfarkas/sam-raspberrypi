from pyfingerprint.pyfingerprint import PyFingerprint
import led.LED as LED
import time

class Fingerprint:

    fingerprint = None
    loading_templates = False
    LCD_pipe = None
    
    def __init__(self):
        try:
            # Try to initialize fingerprint sensor with given password
            self.fingerprint = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
            if (self.fingerprint.verifyPassword() == False):
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)
    
    # Start fingerprint module
    def start(self, parser, main_pipe, LCD_pipe):
        # Setup lcd pipe
        self.LCD_pipe = LCD_pipe
        while 1:
            # Check if there are any updates from parent process
            if main_pipe.poll(1):
                message_from_parent = main_pipe.recv()
                # If parent passed string, it means course id is passed
                # otherwise it's fingerprint templates
                if isinstance(message_from_parent, basestring):
                    # Set course id for parser
                    parser.course_id = message_from_parent
                else:
                    # Load fingerprint templates
                    self.load_templates(message_from_parent)
            # Only try to scan fingers, when sensor is not busy
            if self.loading_templates == False:
                # Try to get finger characteristics
                characteristics = self.get_characteristics()
                if characteristics != None:
                    # If course is not started try to start it
                    # otherwise try to record attendance
                    if parser.course_id == None:
                        # Try to start course
                        course_information = parser.get_course("fingerprint", characteristics)
                        if course_information.error == None:
                            # If course is started and there are fingerprint templates try to load them
                            if course_information.templates != None:
                                self.load_templates(course_information.templates)
                            # Inform user that practical is started
                            LED.asyncGreen()
                            print("started course from finger")
                            LCD_pipe.send("COURSE ID " + course_information.course_id + "                        INITIALIZED")
                            # Tell main process about started practical
                            main_pipe.send(course_information.course_id)
                        else:
                            # Inform user about error
                            print(course_information.error)
                            LED.asyncRed()
                            LCD_pipe.send(course_information.error)
                    else:
                        # Try to record attendance
                        response = parser.record_attendance("fingerprint", characteristics)
                        if response.error == None:
                            # Inform user about recorded attendance
                            LED.asyncGreen()
                            LCD_pipe.send("ID " + response.student_id + "                             RECORDED")
                        else:
                            # Inform user about error
                            LED.asyncRed()
                            print(response.error)
                            LCD_pipe.send("ERROR:                                  " + response.error)
    
    # Loads templates to the fingerprint, expects array of byte strings
    def load_templates(self, templates):
        # Inform other that templates are about to be loaded
        self.loading_templates = True
        print("about to start load")
        # Wait 2 seconds to make sure that no data is beign sent to fingerprint
        time.sleep(2)
        if(self.fingerprint.getTemplateCount() == None):
            return
        print("Preparing to load templates, current count is: " + str(self.fingerprint.getTemplateCount()))
        # Before loading templates remove old ones
        self.fingerprint.clearDatabase()
        print("Deleted old templates, current count is: " + str(self.fingerprint.getTemplateCount()))
        # Create array to store normalized templates
        normalized_templates = []
        # Transfer each template from string to array of ints
        for template in templates:
            normalized_templates.append(map(int, template.split("|")))
        # Go trough normalized templates
        for template in normalized_templates:
            # Load template data to first buffer
            self.fingerprint.uploadCharacteristics(0x01, template)
            # By default code will find free space and store template from first buffer
            # to fingerprint
            self.fingerprint.storeTemplate()
        # Inform module that loading is done
        self.loading_templates = False
        print(normalized_templates)
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
        # Try to read only if not currently loading templates
        if self.loading_templates:
            return None
        # Wait till finger is read
        if (self.fingerprint.readImage() == False):
            return None

        # Converts read image to characteristics and stores it in charbuffer 1
        self.fingerprint.convertImage(0x01)

        # Search template
        result = self.fingerprint.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]
        
        # No match is found
        if (positionNumber == -1):
            LED.asyncRed()
            print("Fingerprint not found")
            self.LCD_pipe.send("FINGERPRINT                             NOT FOUND")
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

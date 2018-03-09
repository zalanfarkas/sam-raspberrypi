from pyfingerprint.pyfingerprint import PyFingerprint
import lcd.LCD as LCD
import led.LED as LED


def start(parser, fingerprint):
    while True:
        characteristics = get_characteristics(fingerprint)
        print(parser.course_id)
        if characteristics == None:
            LED.asyncRed()
            LCD.asyncWrite("Fingerprint not found")
        else:
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
                response = parser.record_attendance("fingerprint", characteristics)
                if response.error == None:
                    LED.asyncGreen()
                    LCD.asyncWrite("Attendance recorded successfully for student with id " + response.student_id)
                else:
                    LED.asyncRed()
                    LCD.asyncWrite("Error: " + response.error)

def load_templates(fingerprint, templates):
    print("Preparing to load templates, current count is: " + str(fingerprint.getTemplateCount()))
    # Before loading templates remove old ones
    fingerprint.clearDatabase()
    print("Deleted old templates, current count is: " + str(fingerprint.getTemplateCount()))
    
    normalized_templates = []
    # Transfer each template from string to array of ints
    for template in course_information.templates:
        normalized_templates.append(map(int, template.split("|")))

    for template in normalized_templates:
        # Load template data to first buffer
        fingerprint.uploadCharacteristics(0x01, template)
        # By default code will find free space and store template from first buffer
        # to fingerprint
        fingerprint.storeTemplate()
    print("Finished loading templates current count is: "+ str(fingerprint.getTemplateCount()))

# Generate template for user
def get_template(fingerprint):
    # Wait for finger
    print('Waiting for finger...')
    while (fingerprint.readImage() == False):
        pass

    # Converts image to characteristic and store it to charbuffer 1
    fingerprint.convertImage(0x01)
    # Retrieves template characteristics as a 512 bytes array
    template = fingerprint.downloadCharacteristics(0x01)
    # Return template as joined string
    return '|'.join(map(str,template))

# Get characteristics
def get_characteristics(fingerprint):
    print('Waiting for finger...')

    # Wait that finger is read
    while (fingerprint.readImage() == False):
        pass
    print("shit")

    # Converts read image to characteristics and stores it in charbuffer 1
    fingerprint.convertImage(0x01)

    # Searchs template
    result = fingerprint.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]
    
    # No match is found
    if (positionNumber == -1):
        return None
    else:
        print('Found template at position #' + str(positionNumber))
        print('The accuracy score is: ' + str(accuracyScore))
        print('Waiting for finger...')
    
    # Loads the found template to charbuffer 1
    fingerprint.loadTemplate(positionNumber, 0x01)
    # Downloads the characteristics of template loaded in charbuffer 1
    template = fingerprint.downloadCharacteristics(0x01)
    # Return template as joined string
    return '|'.join(map(str,template))
            
        

 

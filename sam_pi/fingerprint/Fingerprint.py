from pyfingerprint.pyfingerprint import PyFingerprint

class Fingerprint:

    fingerprint = None
    
    def __init__(self):
        try:
            self.fingerprint = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
            if (self.fingerprint.verifyPassword() == False):
                raise ValueError('The given fingerprint sensor password is wrong!')
        except Exception as e:
            print('The fingerprint sensor could not be initialized!')
            print('Exception message: ' + str(e))
            exit(1)
            
    
    def load_templates(self, templates):
        print("Preparing to load templates, current count is: " + str(self.fingerprint.getTemplateCount()))
        # Before loading templates remove old ones
        self.fingerprint.clearDatabase()
        print("Deleted old templates, current count is: " + str(self.fingerprint.getTemplateCount()))
        

        for template in templates:
            # Load template data to first buffer
            self.fingerprint.uploadCharacteristics(0x01, template)
            # By default code will find free space and store template from first buffer
            # to fingerprint
            self.fingerprint.storeTemplate()
        print("Finished loading templates current count is: "+ str(self.fingerprint.getTemplateCount()))

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

    def testas(self):
        print('Waiting for finger...')

        ## Wait that finger is read
        while ( self.fingerprint.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        self.fingerprint.convertImage(0x01)

        ## Searchs template
        result = self.fingerprint.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber == -1 ):
            print('No match found!')
            exit(0)
        else:
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))

        
        

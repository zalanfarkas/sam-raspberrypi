import time
from network.Parser import Parser
from fingerprint.Fingerprint import Fingerprint
parser = Parser()

# Load templates with other course information
course_information = parser.get_course("nfc", "226198141759")

normalized_templates = []
# Transfer each template from string to array of ints
for template in course_information.templates:
    normalized_templates.append(map(int, template.split("|")))


finerprint_scanner = Fingerprint()
finerprint_scanner.load_templates(normalized_templates)


while True:
    characteristics = finerprint_scanner.get_characteristics()
    
    if characteristics == None:
        print("Fingerprint not found")
        time.sleep(1)
    else:
        response = parser.record_attendance("fingerprint", characteristics)
        if response.error == None:
            print("Attendance recorded successfully for student with id " + response.student_id)
        else:
            print("Error: " + response.error)
        time.sleep(1)


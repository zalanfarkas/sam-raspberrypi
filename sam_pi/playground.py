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


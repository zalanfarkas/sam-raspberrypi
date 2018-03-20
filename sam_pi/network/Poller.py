import time
import led.LED as LED
import lcd.LCD as LCD

class Poller:
    parser = None
    fingerprint_pipe = None
    pi_id = None
    
    # Todo pass fingeprint class as parameter as well
    def __init__(self, parser, fingerprint_pipe, pi_id):
        self.parser = parser
        self.fingerprint_pipe = fingerprint_pipe
        self.pi_id = pi_id
    
    def startPolling(self):
        while 1:
            print("poll")
            self.pollPendingPracticals()
            self.pollCurrentTemplates()
            
     
    def pollPendingPracticals(self):
        if self.parser.course_id == None:
            pending_practical = self.parser.query_pending_practicals(self.pi_id)
            if pending_practical.error != None:
                print("There was an error:" + pending_practical.error)
            elif pending_practical.pending:
                print("Practical for course: " + pending_practical.course_id + " started")
                LED.asyncGreen()
                #LCD.passmessage("COURSE ID " + pending_practical.course_id + "                        INITIALIZED")
                # Inform fingerprint about practical
                fingerprint_pipe.send(pending_practical.course_id)
        time.sleep(10)
        
    def pollCurrentTemplates(self):
        if self.parser.course_id == None:
            upcoming_templates = self.parser.current_templates()
            if upcoming_templates.templates != None:
                # Load templates to fingerprint
                # it would be cool to have a variable inside fingeprint sensor which would tell
                # when was the last time templates were loaded
                # if templates were loaded recently do not call parser.current_templates method
                # i.e add check to first if statement
                self.fingerprint_pipe.send(upcoming_templates.templates)
        time.sleep(60)
        

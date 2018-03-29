# Copyright (c) 2018 Team Foxtrot
# Licensed under MIT License

import time
import led.LED as LED
import lcd.LCD as LCD

class Poller:
    parser = None
    fingerprint_pipe = None
    pi_id = None
    
    # Initialize parser, fingerprint_pipe and pi_id
    def __init__(self, parser, fingerprint_pipe, pi_id):
        self.parser = parser
        self.fingerprint_pipe = fingerprint_pipe
        self.pi_id = pi_id
    
    # Start the polling process
    def startPolling(self):
        while 1:
            self.pollPendingPracticals()
            self.pollCurrentTemplates()
            
    # Polls practicals that are pending
    def pollPendingPracticals(self):
        if self.parser.course_id == None:
            # Try to get pending practicals
            pending_practical = self.parser.query_pending_practicals(self.pi_id)
            if pending_practical.error != None:
                print("There was an error:" + pending_practical.error)
            elif pending_practical.pending:
                print("Practical for course: " + pending_practical.course_id + " started")
                LED.asyncGreen()
                # Inform fingerprint about practical
                self.fingerprint_pipe.send(pending_practical.course_id)
        # Wait 10 seconds
        time.sleep(10)
    
    # Poll fingerprint templates from server
    def pollCurrentTemplates(self):
        # Only poll for fingerprint templates, if practical is not started
        if self.parser.course_id == None:
            # Try to get fingerprint templates
            upcoming_templates = self.parser.current_templates()
            if upcoming_templates.templates != None:
                # Load templates to fingerprint
                self.fingerprint_pipe.send(upcoming_templates.templates)
        # Wait 60 seconds
        time.sleep(60)
        

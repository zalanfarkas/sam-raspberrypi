# Copyright (c) 2018 Team Foxtrot
# Licensed under MIT License

class RecordAttendanceJSON:
    student_id = None
    error = None
    
    def __init__(self, student_id = None, error = None):
        self.student_id = student_id  
        self.error = error

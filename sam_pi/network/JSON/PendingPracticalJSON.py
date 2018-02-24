class PendingPracticalJSON:
    pending = False
    course_id = None
    end_time = None
    error = None
    
    def __init__(self, pending = False, course_id = None, end_time = None, error = None):
        self.pending = pending
        self.course_id = course_id  
        self.end_time = end_time
        self.error = error
    
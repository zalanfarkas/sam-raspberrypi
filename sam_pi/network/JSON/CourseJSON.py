class CourseJSON:
    course_id = None
    end_time = None
    error = None
    templates = None
    
    def __init__(self, course_id = None, end_time = None, templates = None, error = None):
        self.course_id = course_id  
        self.end_time = end_time
        self.error = error
        self.templates = templates
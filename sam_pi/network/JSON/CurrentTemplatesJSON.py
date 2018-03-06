class CurrentTemplatesJSON:
    success = False
    templates = None
    
    def __init__(self, success, templates):
        self.success = success  
        self.templates = templates
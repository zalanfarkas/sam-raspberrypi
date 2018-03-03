class UploadFingerprintJSON:
    success = False
    error = None
    
    def __init__(self, success = False, error = None):
        self.success = success  
        self.error = error
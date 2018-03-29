# Copyright (c) 2018 Team Foxtrot
# Licensed under MIT License

class UploadFingerprintJSON:
    success = False
    error = None
    
    def __init__(self, success = False, error = None):
        self.success = success  
        self.error = error

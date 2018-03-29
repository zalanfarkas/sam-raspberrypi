# Copyright (c) 2018 Team Foxtrot
# Licensed under MIT License

# URL Scheme for API.

# If setting up for first time, change base to your API 
# layer location

class API_URLS:
    BASE = "https://abdn-sam.herokuapp.com/api/"
    GET_COURSE_ID = BASE + "get_course"
    RECORD_ATTENDANCE = BASE + "record_attendance"
    QUERY_PENDING_PRACTICALS = BASE + "pending_practicals"
    UPLOAD_FINGERPRINT = BASE + "upload_fingerprint"
    CURRENT_TEMPLATES = BASE + "current_templates"

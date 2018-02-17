import requests

from CourseJSON import CourseJSON
from RecordAttendanceJSON import RecordAttendanceJSON
from API_URLS import API_URLS

class Parser:
	input_type = None
	data = None
	course_id = None
	
	def __init__(self, input_type = None, data = None, course_id = None):
		self.input_type = input_type  
		self.data = data
		self.course_id = course_id
	
	def get_course(self):
		request = requests.post(API_URLS.GET_COURSE_ID, data = {'type': self.input_type, 'data': self.data})
		
		# Todo: add try catch clause and check for request.status_code to make sure
		# that request is valid
		jsonResponse = request.json()
		
		if jsonResponse['success'] == True:
			course_id = jsonResponse['course_id']
			self.course_id = course_id
			end_time = jsonResponse['end_time']
			return CourseJSON(course_id, end_time)
		else:
			error = jsonResponse['error']
			return CourseJSON(None, None, error)
			
	def record_attendance(self, input_type, data):
		request = requests.post(API_URLS.RECORD_ATTENDANCE, data = {'type': input_type, 'data': data, 'course_id': self.course_id })
		jsonResponse = request.json()
		if jsonResponse['success'] == True:
			student_id = jsonResponse['student_id']
			return RecordAttendanceJSON(student_id)
		else:
			error = jsonResponse['error']
			return RecordAttendanceJSON(None, error)



parser = Parser("nfc", "u00000002")


jsonResp = parser.get_course()
print(jsonResp.error)
print(jsonResp.course_id)
print(jsonResp.end_time)

record_attendance_response = parser.record_attendance("nfc", "u00000002")
print(record_attendance_response.student_id)
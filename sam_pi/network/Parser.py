import requests

from JSON.CourseJSON import CourseJSON
from JSON.RecordAttendanceJSON import RecordAttendanceJSON
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


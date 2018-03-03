import requests

from JSON.CourseJSON import CourseJSON
from JSON.RecordAttendanceJSON import RecordAttendanceJSON
from JSON.PendingPracticalJSON import PendingPracticalJSON
from JSON.UploadFingerprintJSON import UploadFingerprintJSON
from API_URLS import API_URLS

class Parser:
	course_id = None
	# Todo maybe add end_time?
	
	def __init__(self, course_id = None):
		self.course_id = course_id

	def get_course(self, input_type, data):
		request = requests.post(API_URLS.GET_COURSE_ID, data = {'type': input_type, 'data': data})
		
		# Todo: add try catch clause and check for request.status_code to make sure
		# that request is valid
		jsonResponse = request.json()
		
		if jsonResponse['success'] == True:
			course_id = jsonResponse['course_id']
			self.course_id = course_id
			end_time = jsonResponse['end_time']
			templates = jsonResponse['templates']
			return CourseJSON(course_id, end_time, templates)
		else:
			error = jsonResponse['error']
			return CourseJSON(None, None, None, error)
			
	def record_attendance(self, input_type, data):
		request = requests.post(API_URLS.RECORD_ATTENDANCE, data = {'type': input_type, 'data': data, 'course_id': self.course_id })
		jsonResponse = request.json()
		if jsonResponse['success'] == True:
			student_id = jsonResponse['student_id']
			return RecordAttendanceJSON(student_id)
		else:
			error = jsonResponse['error']
			return RecordAttendanceJSON(None, error)

	def query_pending_practicals(self, raspberry_pi_id):
		request = requests.post(API_URLS.QUERY_PENDING_PRACTICALS, data = {'data': raspberry_pi_id })
		jsonResponse = request.json()
		if jsonResponse['success'] == True:
			pending = jsonResponse['pending']
			if pending:
				course_id = jsonResponse['course_id']
				self.course_id = course_id
				end_time = jsonResponse['end_time']
				return PendingPracticalJSON(pending, course_id, end_time)
			return PendingPracticalJSON(pending)
		else:
			error = jsonResponse['error']
			return PendingPracticalJSON(False, None, None, error)
	
	def upload_fingerprint(self, card_id, fingerprint):
		request = requests.post(API_URLS.UPLOAD_FINGERPRINT, data = {'card_id': card_id, 'fingerprint': fingerprint})
		jsonResponse = request.json()
		if jsonResponse['success'] == True:
			return UploadFingerprintJSON(True)
		else:
			error = jsonResponse['error']
			return UploadFingerprintJSON(False, error)
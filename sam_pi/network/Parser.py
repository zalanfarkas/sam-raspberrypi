# Copyright (c) 2018 Team Foxtrot
# Licensed under MIT License

import requests

from JSON.CourseJSON import CourseJSON
from JSON.RecordAttendanceJSON import RecordAttendanceJSON
from JSON.PendingPracticalJSON import PendingPracticalJSON
from JSON.UploadFingerprintJSON import UploadFingerprintJSON
from JSON.CurrentTemplatesJSON import CurrentTemplatesJSON
from API_URLS import API_URLS

class Parser:
	# Internal values to represent state
	course_id = None
	end_time = None
	
	def __init__(self, course_id = None):
		self.course_id = course_id
		
	# Gets course id, end time and fingerprint templates
	def get_course(self, input_type, data):
		# Send post request
		request = requests.post(API_URLS.GET_COURSE_ID, data = {'type': input_type, 'data': data})
		# Convert response to JSON
		jsonResponse = request.json()
		# Fill CourseJSON object with appropriate data
		if jsonResponse['success'] == True:
			course_id = jsonResponse['course_id']
			end_time = jsonResponse['end_time']
			self.course_id = course_id
			self.end_time = end_time
			templates = jsonResponse['templates']
			return CourseJSON(course_id, end_time, templates)
		else:
			error = jsonResponse['error']
			return CourseJSON(None, None, None, error)
	
	# Records the attendance 
	def record_attendance(self, input_type, data):
		# Send post request
		request = requests.post(API_URLS.RECORD_ATTENDANCE, data = {'type': input_type, 'data': data, 'course_id': self.course_id })
		# Convert response to JSON
		jsonResponse = request.json()
		# Fill RecordAttendanceJSON object with appropriate data
		if jsonResponse['success'] == True:
			student_id = jsonResponse['student_id']
			return RecordAttendanceJSON(student_id)
		else:
			error = jsonResponse['error']
			return RecordAttendanceJSON(None, error)
	
	# Retrieves all the practicals that are pending
	def query_pending_practicals(self, raspberry_pi_id):
		# Send post request
		request = requests.post(API_URLS.QUERY_PENDING_PRACTICALS, data = {'data': raspberry_pi_id })
		# Convert response to JSON
		jsonResponse = request.json()
		# Fill PendingPracticalJSON object with appropriate data
		if jsonResponse['success'] == True:
			pending = jsonResponse['pending']
			if pending:
				course_id = jsonResponse['course_id']
				end_time = jsonResponse['end_time']
				self.course_id = course_id
				self.end_time = end_time
				return PendingPracticalJSON(pending, course_id, end_time)
			return PendingPracticalJSON(pending)
		else:
			error = jsonResponse['error']
			return PendingPracticalJSON(False, None, None, error)
	
	# Uploads fingerprint template to the database
	def upload_fingerprint(self, card_id, fingerprint):
		# Send post request
		request = requests.post(API_URLS.UPLOAD_FINGERPRINT, data = {'card_id': card_id, 'fingerprint': fingerprint})
		# Convert response to JSON
		jsonResponse = request.json()
		# Fill UploadFingerprintJSON object with appropriate data
		if jsonResponse['success'] == True:
			return UploadFingerprintJSON(True)
		else:
			error = jsonResponse['error']
			return UploadFingerprintJSON(False, error)
	
	# Method to fetch currently running practicals fingeprint templates		
	def current_templates(self):
		# Send post request
		request = requests.post(API_URLS.CURRENT_TEMPLATES, data = {})
		# Convert response to JSON
		jsonResponse = request.json()
		success = jsonResponse['success']
		templates = jsonResponse['templates']
		# Fill CurrentTemplatesJSON object with appropriate data
		return CurrentTemplatesJSON(success, templates)
		

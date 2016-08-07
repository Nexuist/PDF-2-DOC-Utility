import math, random, time, string, os, traceback
from response import Response
from requests import Request, Session
from requests.exceptions import RequestException, ConnectionError, HTTPError
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

class API:
	def __init__(self, file_path, file_name = ""):
		self.session = Session() # All cookies persist
		self.file_path = file_path
		self.file_name = file_name
		if not file_name:
			self.file_name = os.path.basename(file_path)
		self.file_size = 1
		self.site = "http://pdf2doc.com/"
		self.sid = self.__sid()
		self.fid = self.__fid()
		self.convert_result = None

	def online(self):
		request = Request("GET", self.site)
		response = self.__request(request, json = False)
		return response.successful()

	def upload(self, progress_callback = None):
		# Create request
		path = self.site + "upload/" + self.sid
		formdata = [
			("name", self.file_name),
			("id", self.fid),
			("file", (self.file_name, open(self.file_path, "rb"), "application/pdf"))
		]
		formdata = MultipartEncoder(formdata)
		boundary = formdata.boundary[2:]
		header = {"Content-Type": "multipart/form-data, boundary=" + boundary}
		monitor = MultipartEncoderMonitor(formdata, progress_callback)
		request = Request("POST", path, data = monitor, headers = header)
		response = self.__request(request)
		# Parse response
		if response.successful():
		 	json = response.json
			if "error" in json:
				response.error = "Failed upload: Response contained error"
			elif not "data" in json:
				response.error = "Failed upload: Malformed response"
		# Either the request failed, the response was wrong, or everything worked as intended
		return response

	def convert(self):
		# Create request
		path = self.site + "convert/%s/%s" % (self.sid, self.fid)
		request = Request("GET", path)
		response = self.__request(request)
		# Parse response
		if response.successful():
			json = response.json
			if not "status" in json:
				response.error = "Failed conversion: Malformed response"
			elif json["status"] != "success":
				response.error = "Failed conversion: Website reported conversion failed"
		return response

	def status(self):
		path = self.site + "status/%s/%s" % (self.sid, self.fid)
		request = Request("GET", path)
		response = self.__request(request)
		if response.successful():
			json = response.json
			if not "progress" in json or (json["progress"] == 100 and not "convert_result" in json):
				response.error = "Failed status: Malformed response"
			if json["progress"] == 100:
				self.convert_result = json["convert_result"]
		return response

	def download(self):
		path = self.site + "download/%s/%s/%s" % (self.sid, self.fid, self.convert_result)
		request = Request("GET", path)
		response = self.__request(request, json = False, stream = True)
		return response

	def __request(self, request, json = True, stream = False):
		try:
			request = self.session.prepare_request(request)
			request = self.session.send(request, stream = stream)
			request.raise_for_status()
			if json == True:
				json = request.json()
			else:
				json = None
			return Response(request, json)
		except (AttributeError, ConnectionError, RequestException, Exception) as e:
			if type(e) == AttributeError:
				msg = "Malformed response: Couldn't decode JSON"
			elif type(e) == HTTPError:
				msg = "Server Error: Returned status code " + str(request.status_code)
			elif type(e) == ConnectionError:
				msg = "Network problem: Couldn't reach website"
			elif type(e) == RequestException:
				msg = "Internal error: Requests library error"
			else:
				msg = "Internal error: Uncaught exception"
			return Response(request, error = msg, stack_trace = traceback.format_exc())

	def __base32(self, x):
		# Heavily modified version of https://www.quora.com/How-do-I-write-a-program-in-Python-that-can-convert-an-integer-from-one-base-to-another/answer/Nayan-Shah?srid=uVDVH
		result = ""
		while x > 0:
			result = string.printable[x % 32] + result
			x //= 32
		return result

	def __sid(self):
		chars = "0123456789abcdefghiklmnopqrstuvwxyz"
		result = ""
		for x in xrange(16):
			char = int(math.floor(random.random() * len(chars)))
			result += chars[char:char + 1]
		return result

	def __fid(self):
		uid = self.__base32(int(time.time() * 1000)) # Python equivalent of new Date().getTime().toString(32)
		for x in xrange(5):
			uid += self.__base32(int(math.floor(random.random() * 65535)))
		return "o_" + uid + self.__base32(1)

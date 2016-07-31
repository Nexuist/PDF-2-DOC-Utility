import math, random, time, string, os, traceback
from response import Response
from requests import Request, Session
from requests.exceptions import RequestException, ConnectionError
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

class Upload:
	def __init__(self, file_path, file_name = ""):
		self.session = Session() # All cookies persist
		self.file_path = file_path
		self.file_name = file_name
		if not file_name:
			self.file_name = os.path.basename(file_path)
		self.site = "http://pdf2doc.com/"
		self.sid = self.__sid()
		self.fid = self.__fid()

	def online(self):
		request = Request("GET", self.site)
		response = self.__request(req)
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
		self.upload_size = formdata.len
		header = {"Content-Type": "multipart/form-data, boundary=" + boundary}
		monitor = MultipartEncoderMonitor(formdata, progress_callback)
		request = Request("POST", path, data = monitor, headers = header)
		response = self.__request(req, True)
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
		path = self.site + "convert/%s/%s" % (self.sid, self.fid)
		request = Request("GET", self.site)
		return path

	def status(self):
		pass

	def download(self, file_path):
		pass

	def __request(self, req, return_json = False):
		try:
			request = self.session.prepare_request(req)
			request = self.session.send(req)
			request.raise_for_status()
			json = None
			if return_json == True:
				json = request.json()
			return Response(req, json)
		except (AttributeError, ConnectionError, RequestException, Exception) as e:
			if type(e) == AttributeError:
				msg = "Malformed response: Couldn't decode JSON"
			elif type(e) == ConnectionError:
				msg = "Network problem: Couldn't reach website"
			elif type(e) == RequestException:
				msg = "Internal error: Requests library error"
			elif type(e) == Exception:
				msg = "Internal error: Uncaught exception"
			return Response(req, error = msg, stack_trace = traceback.format_exc())

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

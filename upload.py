import requests, math, random, time, string, os
from requests import Request, Session
from requests.exceptions import RequestException
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

	def __request(self, req, return_json = False):
		try:
			req = self.session.prepare_request(req)
			req = self.session.send(req)
			req.raise_for_status()
			if return_json == True:
				return (True, req.json())
			return (True, req)
		except AttributeError as e:
			return (False, "JSON decoding failed", e)
		except RequestException as e:
			return (False, "Response error", e)
		except Exception as e:
			return (False, "Internal error", e)

	def online(self):
		req = Request("GET", self.site, False)
		response = self.__request(req)
		if response[0] == True:
			return True
		return response


	def upload(self, progress_callback = None):
		try:
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
			req = self.session.post(path, data = monitor, headers = header)
			req.raise_for_status()
			response = req.json()
			print response
			assert not "error" in response, "Response contained error"
			assert "data" in response, "Malformed response"
			return True
		except requests.exceptions.ConnectionError, e:
			return ("Connection error - http://pdf2doc.com or your Internet may be down.", str(e))
		except AssertionError, e:
			return (e, str(response))
		except Exception, e:
			return "Uncaught error: " + str(e)

	def convert(self):
		# try:
		#
		# except Exception, e:
		# 	return e
		pass
	def status(self):
		pass

	def download(self, file_path):
		pass




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

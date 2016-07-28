import requests, math, random, time, string, os
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

class Upload:

	def __init__(self, file_path, file_name = ""):
		self.session = requests.Session() # All cookies persist
		self.file_path = file_path
		self.file_name = file_name
		if not file_name:
			self.file_name = os.path.basename(file_path)
		self.site = "http://pdf2doc.com/"
		self.sid = self.__sid()
		self.fid = self.__fid()

	def online(self):
		try:
			req = self.session.get(self.site)
			req.raise_for_status()
			return True
		except Exception as e:
			return e


	def upload(self, progress_callback = None):
		try:
			path = self.site + "upload/" + self.sid
			params = {
				"name": self.file_name,
				"id": self.fid,
				"file": (self.file_name, open(self.file_path, "rb"), "application/pdf")
			}
			params = MultipartEncoder(params)
			self.upload_size = params.len
			monitor = MultipartEncoderMonitor(params, progress_callback)
			req = self.session.post(path, data = monitor, headers = {"Content-Type": "multipart/form-data"})
			req.raise_for_status()
			return req.content
		except Exception as e:
			return e


	def convert(self):
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

import requests, math, random, time, string

class Uploader:

	def __init__(self, file_path):
		self.file_path = file_path
		self.sid = self.__sid()
		self.fid = self.__fid()

	def upload():
		pass

	def convert():
		pass

	def status():
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

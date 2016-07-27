import requests, math, random, time, string

# upload = requests.get("http://pdf2doc.com")
# print(upload.status_code)


def toBase32(x):
	# Heavily modified version of https://www.quora.com/How-do-I-write-a-program-in-Python-that-can-convert-an-integer-from-one-base-to-another/answer/Nayan-Shah?srid=uVDVH
	result = ""
	while x > 0:
		result = string.printable[x % 32] + result
		x //= 32
	return result

def sid():
	chars = "0123456789abcdefghiklmnopqrstuvwxyz"
	result = ""
	for x in xrange(16):
		char = int(math.floor(random.random() * len(chars)))
		result += chars[char:char + 1]
	return result

def fid():
	uid = toBase32(int(time.time() * 1000)) # Python equivalent of new Date().getTime().toString(32)
	for x in xrange(5):
		uid += toBase32(int(math.floor(random.random() * 65535)))
	return "o_" + uid + toBase32(1)

print(fid())

import requests, math, random

# upload = requests.get("http://pdf2doc.com")
# print(upload.status_code)

def sid():
	chars = "0123456789abcdefghiklmnopqrstuvwxyz"
	result = ""
	for x in xrange(16):
		char = int(math.floor(random.random() * len(chars)))
		result += chars[char:char + 1]
	return result
def fid():
	pass

print(len(sid()))
print(sid())
print(sid())
print(sid())

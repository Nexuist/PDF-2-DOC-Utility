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



def frm(x, b):
    """
    Converts given number x, from base 10 to base b
    x -- the number in base 10
    b -- base to convert
    """
    assert(x >= 0)
    assert(1< b < 37)
    r = ''
    import string
    while x > 0:
        r = string.printable[x % b] + r
        x //= b
    return r
def sid():
	chars = "0123456789abcdefghiklmnopqrstuvwxyz"
	result = ""
	for x in xrange(16):
		char = int(math.floor(random.random() * len(chars)))
		result += chars[char:char + 1]
	return result
def fid():
	timestamp = int(time.time() * 1000) # Python equivalent of new Date().getTime()
	return toBase32(timestamp)

print(fid())
print(fid())
print(fid())

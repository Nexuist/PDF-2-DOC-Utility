from __future__ import division
from upload import Upload

test = Upload("Test.pdf")

def progress(monitor):
	print monitor.bytes_read / test.upload_size

if test.online():
	print("Online!")
	upload = test.upload()
	print(upload.successful())
	print(upload.error)
	print(upload.json)
else:
	print("Offline!")

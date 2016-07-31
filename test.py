from __future__ import division
from upload import Upload

test = Upload("Test.pdf")

def print_response(response):
	print("Successful: %s" % response.successful())
	print("Response: %s" % response.json)
	print("Error: %s" % response.error)
	print("Stack Trace: ")
	print(response.stack_trace)

def progress(monitor):
	percent = (monitor.bytes_read / test.upload_size) * 100
	print("%.2f" % percent)

if test.online():
	print("### Uploading ###")
	print_response(test.upload(progress))
	print("### Converting ###")
	print_response(test.convert())
else:
	print("Offline!")

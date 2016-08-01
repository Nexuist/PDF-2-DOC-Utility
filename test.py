from __future__ import division
import time
from upload import Upload

test = Upload("Test.pdf")

def print_response(response):
	print("Response: %s" % response.json)
	if response.error:
		print("Error: %s" % response.error)
		print("Stack Trace: ")
		print(response.stack_trace)

def progress(monitor):
	percent = (monitor.bytes_read / test.upload_size) * 100
	print("Upload progress: %.2f" % percent)

if test.online():
	print("### Uploading ###")
	print_response(test.upload(progress))
	print("### Requesting Conversion ###")
	print_response(test.convert())
	print("### Converting ###")
	stop = False
	status = None
	while not stop:
		status = test.status()
		if not status.successful():
			stop = True
			break
		progress = status.json["progress"]
		if progress == 100:
			if "convert_result" not in status.json:
				status.error = "Failed status: Malformed response"
			stop = True
			break
		else:
			print("Progress: %s" % progress)
		time.sleep(1)
	print_response(status)
	if status.successful():
		print("### Downloading ###")
		file_path = status.json["convert_result"]
		print("Saving to file: %s" % file_path)
		test.download(file_path)

	else:
		print("Failed to retrieve status")
else:
	print("Offline!")

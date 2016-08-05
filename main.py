from __future__ import division
from ui import UI
from upload import Upload
import sys, os

def print_response(response):
	print("Response: %s" % response.json)
	if response.error:
		print("Error: %s" % response.error)
		print("Stack Trace: ")
		print(response.stack_trace)

def routine():
	if len(sys.argv) != 2 or not sys.argv[1].lower().endswith(".pdf"):
		ui.info("Drag a PDF on top of the application to begin converting it.")
	elif not os.path.isfile(sys.argv[1]):
		ui.error("Incompatible File", "The file that was dragged onto the application cannot be converted. Make sure it is in PDF format.")
	file_name = sys.argv[1]
	upload = Upload(file_name)
	if not upload.online():
		ui.error("Network Failure", "Couldn't reach http://pdf2doc.com - Perhaps the website or your Internet is down.")
	ui.set_micro("Website online. Beginning upload...", 0)
	upload_size = 1
	def progress(monitor):
		text = "Uploading... %s / %s bytes" % (monitor.bytes_read, monitor.len)
		percent = (monitor.bytes_read / monitor.len) * 100
		ui.set_micro(text, percent)
	response = upload.upload(progress)
ui = UI()
ui.root.after(500, routine)
ui.render()

from __future__ import division
from ui import UI
from upload import Upload
from response import Response
import sys, os

global VERBOSE
VERBOSE = False

def debug(msg):
	if not VERBOSE:
		return
	if isinstance(msg, Response):
		print("Response: %s" % msg.json)
		if msg.error:
			print("Error: %s" % msg.error)
			print("Stack Trace: ")
			print(msg.stack_trace)
	else:
		print msg

def main():
	if len(sys.argv) < 2 or not sys.argv[1].lower().endswith(".pdf"):
		ui.info("Drag a PDF on top of the application to begin converting it.")
	elif not os.path.isfile(sys.argv[1]):
		ui.error("Incompatible File", "The file that was dragged onto the application cannot be converted. Make sure it is in PDF format.")
	if len(sys.argv) >= 2 and sys.argv[2] == "-v":
		global VERBOSE
		VERBOSE = True
		debug("Verbose mode activated")
	file_name = sys.argv[1]
	debug("Using file name: %s" % file_name)
	upload = Upload(file_name)
	ui.set_micro("Ensuring connectivity...", 0)
	ui.set_macro("(1/3) Uploading PDF... ", 33)
	if not upload.online():
		ui.error("Network Failure", "Couldn't reach http://pdf2doc.com - Perhaps the website or your Internet is down.")
	ui.set_micro("Website online. Beginning upload...", 0)
	def progress(monitor):
		text = "Uploading... %s / %s bytes" % (monitor.bytes_read, monitor.len)
		percent = (monitor.bytes_read / monitor.len) * 100
		ui.set_micro(text, percent)
	response = upload.upload(progress)
	debug("UPLOAD:")
	debug(response)
	if response.error:
		ui.error("Upload Failure", "Error: %s" % response.error)
	ui.set_macro("(2/3) Converting...", 33)
	ui.set_micro("Requesting conversion...", 0)
	response = upload.convert()
	debug("CONVERT:")
	debug(response)
	if response.error:
		ui.error("Conversion Failure", "Error: %s" % response.error)



ui = UI()
ui.root.after(500, main)
ui.render()

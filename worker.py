from threading import Thread
from ui import UI
from api import API
import sys, random, time, os

class Worker(Thread):
	def __init__(self, ui):
		Thread.__init__(self)
		self.ui = ui

	def debug(self, res):
		print("Response: %s" % res.json)
		if res.error:
			print("Error: %s" % res.error)
			print("Stack Trace: ")
			print(res.stack_trace)

	def run(self):
		if len(sys.argv) < 2 or not sys.argv[1].lower().endswith(".pdf"):
			self.ui.error("No File Given", "Drag a PDF on top of the application to begin converting it.")
			return
		elif not os.path.isfile(sys.argv[1]):
			self.ui.error("Incompatible File", "The file that was dragged onto the application cannot be converted. Make sure it is in PDF format.")
			return
		converter = API(sys.argv[1])
		# ENSURE CONNECTIVITY
		self.ui.set_micro("Ensuring connectivity...", 0)
		self.ui.set_macro("(1/3) Uploading PDF... ", 33)
		if not converter.online():
			self.ui.error("Network Failure", "Couldn't reach http://pdf2doc.com - Perhaps the website or your Internet is down.")
			return
		self.ui.set_micro("Website online. Beginning upload...", 0)
		# UPLOAD
		def progress(monitor): # Callback for upload progress
			text = "Uploading... %s / %s bytes" % (monitor.bytes_read, monitor.len)
			percent = (monitor.bytes_read / monitor.len) * 100
			self.ui.set_micro(text, percent)
		response = converter.upload(progress)
		print "UPLOAD"
		self.debug(response)
		if not response.successful():
			self.ui.error("Upload Failure", "Error: %s" % response.error)
			return
		# REQUEST CONVERSION
		self.ui.set_micro("Requesting conversion...", 0)
		self.ui.set_macro("(2/3) Converting...", 33)
		response = converter.convert()
		print "CONVERT"
		self.debug(response)
		if not response.successful():
			self.ui.error("Conversion Failure", "Monitor Error: %s" % response.error)
			return
		# MONITOR CONVERSION
		self.ui.set_micro("Monitoring conversion...", 0)
		stop = False
		while not stop:
			response = converter.status()
			print "MONITOR CONVERT"
			self.debug(response)
			if not response.successful():
				self.ui.error("Conversion Failure", "Status Error: %s" % response.error)
				return
			progress = response.json["progress"]
			self.ui.set_micro("Monitoring conversion...", progress)
			if progress == 100:
				stop = True
				break
			time.sleep(1)
		# DOWNLOAD
		self.ui.set_micro("Sending download request...", 0)
		self.ui.set_macro("(3/3) Downloading DOC...", 100)
		response = converter.download()
		print "DOWNLOAD"
		self.debug(response)
		request = response.request
		if not response.successful():
			self.ui.error("Download Failure", "Request Error: %s"  % response.error)
			return
		try:
			self.ui.set_micro("Opening file...", 0)
			doc = open(converter.convert_result, "wb")
			self.ui.set_micro("Writing to file...", 0)
			with doc:
				for chunk in request.iter_content(chunk_size = 1024):
					doc.write(chunk)
			request.close()
		except IOError as e:
			self.ui.error("Download Failure", "IOError: %s" % str(e))
			return
		except Exception as e:
			self.debug(traceback.format_exc())
			self.ui.error("Download Failure", "Uncaught Exception: %s" % str(e))
			return
		print "DONE"
		self.ui.quit()

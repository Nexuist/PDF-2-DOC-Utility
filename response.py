class Response:
	def __init__(self, request, json = None, error = None, stack_trace = None):
		self.request = request
		self.json = json
		self.error = error
		self.stack_trace = stack_trace

	def successful(self):
		return self.error == None

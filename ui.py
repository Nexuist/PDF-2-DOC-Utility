from Tkinter import *
from ttk import *
import tkMessageBox, sys, Queue

# Threading and queue ideas gratefully provided by http://stupidpythonideas.blogspot.com/2013/10/why-your-gui-app-freezes.html

class UI:
	def __init__(self):
		self.root = root = Tk()
		root.title("PDF 2 Doc Utility")
		root.resizable(width = False, height = False)
		frame = Frame(width = 500, height = 200)
		frame.grid()
		micro_label = Label(frame)
		micro_label.grid(row = 1, sticky = "w", padx = 25, pady = 10)
		micro_bar = Progressbar(frame, length = 400)
		micro_bar.grid(row = 2, padx = 25)
		macro_label = Label(frame)
		macro_label.grid(row = 3, sticky = "w", padx = 25, pady = 10)
		macro_bar = Progressbar(frame, length = 400)
		macro_bar.grid(row = 4, padx = 25, pady = 10)
		self.micro_label = micro_label
		self.micro_bar = micro_bar
		self.macro_label = macro_label
		self.macro_bar = macro_bar
		self.should_quit = False
		self.queue = Queue.Queue()

	def schedule(self, func):
		self.queue.put(func)

	def render(self):
		if self.should_quit:
			self.root.destroy()
			sys.exit(0)
		while True:
			try:
				command = self.queue.get(block = False)
			except Queue.Empty:
				break
			else:
				self.root.after_idle(command)
		self.root.after(100, self.render)

	def start(self):
		self.root.after(100, self.render)
		self.root.mainloop()

	def quit(self):
		self.should_quit = True

	def set_micro(self, text, value):
		self.schedule(lambda: self.micro_label.config(text = text))
		self.schedule(lambda: self.micro_bar.config(value = value))

	def set_macro(self, text, value):
		self.schedule(lambda: self.macro_label.config(text = text))
		self.schedule(lambda: self.macro_bar.config(value = value))

	def error(self, title, msg):
		self.schedule(lambda: tkMessageBox.showerror(title, msg))
		self.set_micro("Error - restart application.", 0)
		self.set_macro("", 0)

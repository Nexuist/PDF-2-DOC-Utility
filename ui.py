from Tkinter import *
from ttk import *
import tkMessageBox

class UI:
	def __init__(self):
		self.root = root = Tk()
		root.title("PDF 2 Doc Utility")
		root.resizable(width = False, height = False)
		frame = Frame(width = 500, height = 200)
		frame.grid()
		micro_label = Label(frame, text = "Ensuring connectivity...")
		micro_label.grid(row = 1, sticky = "w", padx = 25, pady = 10)
		micro_bar = Progressbar(frame, length = 400)
		micro_bar.grid(row = 2, padx = 25)
		macro_label = Label(frame, text = "(1/4) Upload PDF...")
		macro_label.grid(row = 3, sticky = "w", padx = 25, pady = 10)
		macro_bar = Progressbar(frame, length = 400)
		macro_bar.grid(row = 4, padx = 25, ipady = 10)
		self.micro_label = micro_label
		self.micro_bar = micro_bar
		self.macro_label = macro_label
		self.macro_bar = macro_bar

	def set_micro(self, text, value):
		self.micro_label.config(text = text)
		self.micro_bar.config(value = value)

	def set_macro(self, text, value):
		self.macro_label.config(text = text)
		self.macro_bar.config(value = value)

	def info(self, msg):
		tkMessageBox.showinfo("Information", msg)
		self.quit()

	def error(self, title, msg):
		tkMessageBox.showerror(title, msg)
		self.quit()

	def render(self):
		self.root.mainloop()

	def quit(self):
		self.root.destroy()

from Tkinter import *
from ttk import *
import pygubu

def main():
	root = Tk()
	root.title("The pdf2doc Utility")
	root.resizable(width = False, height = False)
	main = Frame(width = 500, height = 200)
	main.grid()
	micro_label = Label(main, text = "Uploading...")
	micro_label.grid(row = 1, sticky = "w", padx = 25, pady = 10)
	micro_bar = Progressbar(main, length = 400)
	micro_bar.grid(row = 2, padx = 25)
	macro_label = Label(main, text = "Testing...")
	macro_label.grid(row = 3, sticky = "w", padx = 25, pady = 10)
	macro_bar = Progressbar(main, length = 400)
	macro_bar.grid(row = 4, padx = 25, ipady = 10)
	print("Ready")
	root.mainloop()

if __name__ == '__main__':
  main()

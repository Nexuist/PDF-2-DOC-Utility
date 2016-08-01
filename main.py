from Tkinter import *
from ttk import *
import pygubu

def main():
	root = Tk()
	root.resizable(width = False, height = False)
	root.geometry("500x200")
	frame = Frame(root)
	frame.pack(fill = BOTH, expand = YES)
	label = Label(frame, text = "Downloading document...")
	label.pack(side = TOP)
	progress = Progressbar(frame, length = 100)
	progress.pack(side = BOTTOM)
	print("Ready")
	root.mainloop()

if __name__ == '__main__':
  main()

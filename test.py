from upload import Upload

a = Upload("Test.pdf")
if a.online():
	print("Online!")

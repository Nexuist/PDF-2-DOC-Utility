from __future__ import division
from upload import Upload

a = Upload("Test.pdf")
print(a.sid)
print(a.fid)
print(a.file_name)
def test(monitor):
	print monitor.bytes_read / a.upload_size
if a.online():
	print(a.upload(test))

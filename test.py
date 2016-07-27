import requests

upload = requests.get("http://pdf2doc.com")
print(upload.status_code)

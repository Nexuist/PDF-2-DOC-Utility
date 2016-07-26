### Backstory

The website http://pdf2doc.com/ offers the ability to convert PDF files to Word documents online. During testing, it was found to be a better converter than many other online and offline alternatives. I wanted to develop a local client that utilized this website behind the scenes.

### Goal

Discover how a browser interacts with pdf2doc.com and reverse engineer a solution that does not require a browser.

### Tools

A combination of the Chrome Developer Tools and the `curl` command line utility were used to conduct this research.

### Discoveries

* The website uses the [Plupload](https://github.com/moxiecode/plupload) API to handle file uploads and progress notifications.

* Uploads and progress notifications are done through AJAX - the page never reloads.

* Upon page load, a 16 character session ID (`sid`) is generated using the following method:
	```javascript
	function randomString() {
	    for (var t = "0123456789abcdefghiklmnopqrstuvwxyz", e = 16, i = "", n = 0; e > n; n++) {
	        var a = Math.floor(Math.random() * t.length);
	        i += t.substring(a, a + 1)
	    }
	    return i
	}
	```
	> http://pdf2doc.com/common/js/common.min.js

* Before uploading, the [Plupload](https://github.com/moxiecode/plupload) library generates a ~30 character unique file ID (`fid`) using the following method:
	```javascript
	var guid = (function() {
		var counter = 0;

		return function(prefix) {
			var guid = new Date().getTime().toString(32), i;

			for (i = 0; i < 5; i++) {
				guid += Math.floor(Math.random() * 65535).toString(32);
			}

			return (prefix || 'o_') + guid + (counter++).toString(32);
		};
	}());
	```
	>https://github.com/moxiecode/plupload/blob/e8b7cc3535cb25f7148366ee8987c72ce127daed/js/moxie.js#L386-#L410

* The upload process begins when a POST request with Content-Type of "multipart/form-data" is sent to the `/upload/<sid>` endpoint. The request also contains three parameters:
	* `name` The filename, ex. "test.pdf"
	* `id` The file ID (`fid`)
	* `file` The file itself, in binary format.

	> **NOTES:** Although `sid` and `fid` are generated using the methods above, the fact that they are created client-side means that you can substitute your own values if you so wish. `fid` appears to accept any value, while `sid` must be 16 characters in order to be processed.

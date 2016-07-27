### Backstory

The website http://pdf2doc.com/ offers the ability to convert PDF files to Word documents online. During testing, it was found to be a better converter than many other online and offline alternatives. I wanted to develop a local client that utilized this website behind the scenes.

### Goal

Discover how a browser interacts with pdf2doc.com and reverse engineer a solution that does not require a browser.

### Tools

A combination of the Chrome Developer Tools and the `curl` command line utility were used to conduct this research.

### Discoveries

* The website uses the [Plupload](https://github.com/moxiecode/plupload) API to handle file uploads.

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

	> **NOTE:** Although `sid` and `fid` are generated using the methods above, the fact that they are created client-side means that you can substitute your own values if you so wish. `fid` appears to accept any value, while `sid` must be 16 characters long in order to be processed.

	An example `curl` looks like this:

	```
	curl -X POST -F "name=ID-Test.pdf" -F "id=testing" -F "file=@Test.pdf" -H "Content-Type: multipart/form-data" http://pdf2doc.com/upload/3sw4i3wpq25qm46s
	```

	The response is sent as JSON and looks like this:

	```json
	{
		"data": {
			"file": "Test.pdf",
			"file_size_human": "74K"
		},
		"id": "testing",
		"jsonrpc": "2.0",
		"result": null
	}
	```
* Immediately after uploading, the page sends a GET request to `/convert/<sid>/<fid>?rnd=<rnd>`. `rnd` appears to just be a value generated using `Math.random()` and has no significance to the request (it can be omitted without consequence). I believe `rnd` simply acts as a cache-busting mechanism.

	An example `curl` looks like this:

	```
	curl http://pdf2doc.com/convert/3sw4i3wpq25qm46s/testing
	```

	And the response:

	```json
	{"status": "success"}
	```

	I wasn't able to get a conversion to fail (I didn't really try) but it is certainly possible - and if it does, this is probably where you can find out.

* The conversion can be monitored through the `/status/<sid>/<fid>?rnd=<rnd` endpoint. `rnd` serves the same purpose here as it did previously.

	An example `curl` looks like this:

	```
	curl http://pdf2doc.com/status/3sw4i3wpq25qm46s/testing
	```

	Response:

	```json
	{
		"fid": "testing",
		"progress": 0,
		"sid": "3sw4i3wpq25qm46s",
		"status": "processing",
		"status_text": null
	}
	```

	Presumably, `progress` changes over time to reflect how close the conversion is to being completed. In addition, the JSON format changes once the conversion is completed:

	```json
	{
		"convert_result": "Test.doc",
		"fid": "testing",
		"progress": 100,
		"savings": null,
		"sid":" 3sw4i3wpq25qm46s",
		"status": "success",
		"thumb_url": "\/files\/3sw4i3wpq25qm46s\/testing\/thumb.png?nimg"
	}
	```
	`convert_result` is the filename of the newly converted document. `thumb_url` is a URI leading to a 125x77 screenshot of the converted document. The query (`nimg`) appears to be another randomly generated cache-busting mechanism.

	> **NOTE:** If you visit this endpoint before  hitting the previous one, you will get the following error:

	```json
	{
		"details": "Conversion error.",
		"status": "error"
	}
	```

	> This does not actually mean the conversion failed, it just means that it was never started. Apparently, you have to trigger the conversion manually.


* Finally, to download the file, the page sends a GET request to `/download/<sid>/<fid>/<convert_result>?rnd=<rnd`. This link is generated in an anonymous function assigned as a click event handler:

	```javascript
	$("#" + data.fid + " div.plupload_file_button" + (thumbnail_clickable ? ", #" + data.fid + " .plupload_thumb" : "")).click(function() {
			downloadURI("download/" + data.sid + "/" + data.fid + "/" + data.convert_result + "?rnd=" + Math.random(), data.convert_result);
	});
	```

	And here's the source for `downloadURI`:
	```javascript
	function downloadURI(uri, name) {
	    if (HTMLElement.prototype.click) {
	        var link = document.createElement("a");
	        link.download = name;
	        link.href = uri;
	        link.style.display = "none";
	        document.body.appendChild(link);
	        link.click();
	        setTimeout(function() { link.remove(); }, 500);
	    } else {
	        window.location.href = uri;
	    }
	}
	```
	> http://pdf2doc.com/js/main.js

	Example `curl`:

	```
	curl http://pdf2doc.com/download/3sw4i3wpq25qm46s/testing/Test.doc
	```

	The response is, of course, the file itself.

### Conclusion

* There are four main API endpoints:
	* `/upload`
	* `/convert`
	* `/status`
	* `/download`

* Every endpoint uses a combination of a session ID (`sid`) and file ID (`fid`) which are both generated client-side.
* There is no form of authentication.
* There may be rate-limiting, but I don't expect this tool to be used so frequently by its users that rate-limiting actually becomes a problem.

### Next Steps

I will be using Python 2.7 with the [requests]() library to automate this process. In addition, I will utilize [Tkinter]() and [py2exe]() to package the software into a Windows executable with a GUI.

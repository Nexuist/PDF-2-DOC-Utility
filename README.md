### Introduction

The website http://pdf2doc.com/ offers the ability to convert PDF files to Word documents online. During testing, it was found to be a better converter than many other online and offline alternatives. I wanted to develop a local client that utilized this website behind the scenes.

### Dependencies

* [Python 2.7+](https://www.python.org/downloads/)
	* Comes preinstalled on most Linux and OS X versions
* [requests](http://docs.python-requests.org/en/master/)
	* `pip install requests`

* [requests-toolbelt](https://github.com/sigmavirus24/requests-toolbelt)
	* `pip install requests-toolbelt`

Windows and OS X binaries will be available soon.

[//]: # "Make sure UI looks right!"

### Usage

Via console:
>python main.py pdf

Alternatively, in Windows, you can simply drag a PDF over `main.py` to begin the procedure. This is because, in Windows, any file dragged over an executable is added as a command line argument.

The file must end in `pdf`. The software will open up a window where you can view the progress of the conversion and any errors that may be encountered. Finally, the converted `doc` will be downloaded and placed into the same directory as the executable.

### Exploration

The process of reverse engineering http://pdf2doc.com/ was outlined in [EXPLORATION.md](/EXPLORATION.md).

### Next Steps

* Simplify code?

* Windows release

* OS X release?
	* Can be done with py2app
	* OS X already comes with Python, so the only trouble saved will be through avoiding dependencies

### License

```
MIT License

Copyright (c) 2016 Andi Andreas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

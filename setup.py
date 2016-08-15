from distutils.core import setup
import py2exe

setup(
    windows = ["main.py"],
    options = {
        "py2exe": {
            "optimize": 2,
            "compressed": True,
            "ascii": False
        }
    }
)

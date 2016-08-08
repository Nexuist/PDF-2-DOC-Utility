from __future__ import division
from worker import Worker
from ui import UI
import time

ui = UI()
worker = Worker(ui)
ui.root.after(500, lambda: worker.start())
ui.start()

from __future__ import division
from worker import Worker
from ui import UI

ui = UI()
worker = Worker(ui)
ui.root.after(500, lambda: worker.start())
ui.start()

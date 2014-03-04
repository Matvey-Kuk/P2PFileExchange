__author__ = 'lossidze'

from openfile  import diffile
from threading import Thread

class threadControl(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.dif = diffile()
    def run(self):
        self.dif.find_diff()

thread = threadControl()
thread.start()

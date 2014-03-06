
from openfile  import Diffile
from threading import Thread

class threadControl(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.dif = Diffile()
    def run(self):
        self.dif.find_diff()

thread = threadControl()
thread.start()

<<<<<<< HEAD
__author__ = 'lossidze'

from openfile  import diffile
=======

from openfile  import Diffile
>>>>>>> Cotl
from threading import Thread

class threadControl(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
<<<<<<< HEAD
        self.dif = diffile()
=======
        self.dif = Diffile()
>>>>>>> Cotl
    def run(self):
        self.dif.find_diff()

thread = threadControl()
thread.start()

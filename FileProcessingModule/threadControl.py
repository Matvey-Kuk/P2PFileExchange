__author__ = 'lossidze'

from openfile  import diffile
from threading import Thread

class threadControl(Thread):
	"""Выделяем поток по заданную задачу"""
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.dif = diffile()
    def run(self):
        self.dif.find_diff()

if ("__name__" == "__main__"):
	thread = threadControl()
	thread.start()

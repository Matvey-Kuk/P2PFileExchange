
from openfile import FilesDifferences
from threading import Thread


class ThreadControl(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.dif = FilesDifferences('base')
    def run(self):
        pass

thread = ThreadControl()
thread.start()

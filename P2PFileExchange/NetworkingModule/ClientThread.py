import threading
from .ThreadStopException import *

threading.SystemExit = SystemExit, ThreadStopException


class ClientThread(threading.Thread):

    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        raise NotImplementedError("Эту функцию необходимо унаследовать")

    def stop(self):
        raise ThreadStopException()
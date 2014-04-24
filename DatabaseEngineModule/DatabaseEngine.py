from DatabaseEngineModule2.SynchronizableDatabase import *


class DatabaseEngine(SynchronizableDatabase):
    """
    База данных, которая умеет работать с сетью.
    """

    def __init__(self, networking, requests_processor):
        self.__networking = networking
        self.__requests_processor = requests_processor
        super().__init__()
        self.process()

    def process(self):
        pass
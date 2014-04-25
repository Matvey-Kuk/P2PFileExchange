from threading import Timer

from DatabaseEngineModule.SynchronizableDatabase import *


class DatabaseEngine(SynchronizableDatabase):
    """
    База данных, которая умеет работать с сетью.
    """

    def __init__(self, networking, requests_processor):
        self.__networking = networking
        self.__requests_processor = requests_processor
        super().__init__()
        self.process()
        self.__register_callbacks()

    def process(self):
        update_timeout = 5

        self.insert_alteration(Alteration(
            {
                random.randint(0, 10): random.randint(100, 999)
            },
            VersionsRange(version=self.get_last_version() + 1)
        ))

        print('Database:' + repr(self))

        timer = Timer(update_timeout, self.process)
        timer.start()

    def __register_callbacks(self):
        pass
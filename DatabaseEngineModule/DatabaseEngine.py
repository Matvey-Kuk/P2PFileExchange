from threading import Timer

from DatabaseEngineModule.SynchronizableDatabase import *
from NetworkingModule.NetworkingUsingModule import *


class DatabaseEngine(SynchronizableDatabase, NetworkingUsingModule):
    """
    База данных, которая умеет работать с сетью.
    """

    def __init__(self, networking, requests_processor):
        self.__networking = networking
        self.__requests_processor = requests_processor
        SynchronizableDatabase.__init__(self)
        NetworkingUsingModule.__init__(self, networking, requests_processor, 'database_engine')
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
        # self.register_request_answer_generator('server_port', self.server_port_request_answer)
        # self.register_answer_received_callback('server_port', self.server_port_answer_received)
        pass
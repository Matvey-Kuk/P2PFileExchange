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
        self.__process()
        self.__register_callbacks()

        self.__peers_to_databases_ids = {}

    def __process(self):
        update_timeout = 5

        self.insert_alteration(Alteration(
            {
                random.randint(0, 10): random.randint(100, 999)
            },
            VersionsRange(version=self.get_last_version() + 1)
        ))

        print('Database:' + repr(self))

        self.__request_databases_conditions()

        timer = Timer(update_timeout, self.__process)
        timer.start()

    def __register_callbacks(self):
        self.register_request_answer_generator('database_condition', self.__database_condition_answer_generator)
        self.register_answer_received_callback('database_condition', self.__database_condition_answer_received)

    def __database_condition_answer_generator(self, question_data):
        print('database_request_received' + repr(question_data))


    def __database_condition_answer_received(self, request):
        print('database_answer_received')

    def __request_databases_conditions(self):
        for peer in self.__networking.get_peers():
            database_id = self.get_peer_metadata(peer, 'database_id')
            versions_ranges = self.get_versions_ranges_required_from_another_database(database_id)
            dumped_versions_ranges = []
            for versions_range in versions_ranges:
                dumped_versions_ranges.append(versions_range.get_dump())
            self.send_request(peer, 'database_condition', dumped_versions_ranges)
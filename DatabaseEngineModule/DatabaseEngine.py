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
        update_timeout = 2

        self.insert_alteration(Alteration(
            {
                str(random.randint(0, 10)): str(random.randint(100, 999))
            },
            VersionsRange(version=self.get_last_version() + 1)
        ))

        print('Database:' + repr(self))

        self.__request_databases_conditions()
        self.__request_needed_alterations()

        timer = Timer(update_timeout, self.__process)
        timer.start()

    def __register_callbacks(self):
        self.register_request_answer_generator('database_condition', self.__database_condition_answer_generator)
        self.register_answer_received_callback('database_condition', self.__database_condition_answer_received)

        self.register_request_answer_generator('alterations', self.__get_alterations_answer_generator)
        self.register_answer_received_callback('alterations', self.__get_alterations_answer_received)

    def __database_condition_answer_generator(self, dumped_versions_ranges):
        versions_ranges = []
        for dumped_versions_range in dumped_versions_ranges:
            versions_ranges.append(VersionsRange(dump=dumped_versions_range))
        result_conditions = []
        for versions_range in versions_ranges:
            result_conditions.append(self.get_condition(versions_range))
        return result_conditions

    def __database_condition_answer_received(self, request):
        conditions = request.answer_data
        if self.get_peer_metadata(request.peer, 'database_id') is None:
            self.set_peer_metadata(request.peer, 'database_id', conditions[0]['id'])
        for condition in conditions:
            self.notify_condition(condition)

    def __request_databases_conditions(self):
        for peer in self.__networking.get_peers():
            database_id = self.get_peer_metadata(peer, 'database_id')
            versions_ranges = self.get_versions_ranges_required_from_another_database(database_id)
            dumped_versions_ranges = []
            for versions_range in versions_ranges:
                dumped_versions_ranges.append(versions_range.get_dump())
            self.send_request(peer, 'database_condition', dumped_versions_ranges)

    def __request_needed_alterations(self):
        for peer in self.__networking.get_peers():
            database_id = self.get_peer_metadata(peer, 'database_id')
            if not database_id is None:
                versions_ranges = self.get_versions_ranges_for_required_from_foreign_database_alterations(database_id)
                dumped_versions_ranges = []
                for versions_range in versions_ranges:
                    dumped_versions_ranges.append(versions_range.get_dump())
                print('sending req ' + repr(dumped_versions_ranges))
                self.send_request(peer, 'alterations', dumped_versions_ranges)

    def __get_alterations_answer_generator(self, dumped_versions_ranges):
        alterations = []
        for dumped_versions_range in dumped_versions_ranges:
            alterations += self.get_alterations(VersionsRange(dump=dumped_versions_range))
        dumped_alterations = []
        for alteration in alterations:
            dumped_alterations.append(alteration.get_dump())
        return dumped_alterations

    def __get_alterations_answer_received(self, request):
        print('Alterations received: ' + repr(request.answer_data))
        dumped_alterations = request.answer_data
        alterations = []
        for dumped_alteration in dumped_alterations:
            alterations.append(Alteration.serialize_from_dump(dumped_alteration))
        for alteration in alterations:
            self.insert_alteration(alteration)
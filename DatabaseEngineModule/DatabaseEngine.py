from threading import Timer

from DatabaseEngineModule.SynchronizableDatabase import *
from NetworkingModule.NetworkingUsingModule import *
from Interface.Interface import *
from Interface.AllowingProcessing import *


class DatabaseEngine(SynchronizableDatabase, NetworkingUsingModule):
    """
    База данных, которая умеет работать с сетью.
    """

    def __init__(self, networking, requests_processor, prefix):
        self.__networking = networking
        self.__requests_processor = requests_processor
        SynchronizableDatabase.__init__(self)
        NetworkingUsingModule.__init__(self, networking, requests_processor, prefix)
        self.__process()
        self.__register_callbacks()
        self.__register_interface_callbacks()

        self.__peers_to_databases_ids = {}

    def __process(self):
        if not AllowingProcessing.allow_processing:
            return 0

        update_timeout = 2

        # self.insert_alteration(Alteration(
        #     {
        #         str(random.randint(0, 10)): str(random.randint(100, 999))
        #     },
        #     VersionsRange(version=self.get_last_version() + 1)
        # ))
        #
        # print('Database:' + repr(self))

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
        for peer in self.__get_peers_database_working_with():
            database_id = self.get_peer_metadata(peer, 'database_id')
            versions_ranges = self.get_versions_ranges_required_from_another_database(database_id)
            dumped_versions_ranges = []
            for versions_range in versions_ranges:
                dumped_versions_ranges.append(versions_range.get_dump())
            self.send_request(peer, 'database_condition', dumped_versions_ranges)

    def __request_needed_alterations(self):
        for peer in self.__get_peers_database_working_with():
            database_id = self.get_peer_metadata(peer, 'database_id')
            if not database_id is None:
                versions_ranges = self.get_versions_ranges_for_required_from_foreign_database_alterations(database_id)
                dumped_versions_ranges = []
                for versions_range in versions_ranges:
                    dumped_versions_ranges.append(versions_range.get_dump())
                # print_str = ''
                # for dumped_versions_range in dumped_versions_ranges:
                #     print_str += repr(dumped_versions_range)
                #     print_str += repr(self.get_hash(VersionsRange(first=dumped_versions_range['first'], last=dumped_versions_range['last'])))
                #     print_str += repr(Alteration.merge(self.get_alterations(VersionsRange(first=dumped_versions_range['first'], last=dumped_versions_range['last']))))
                #     print_str += '\n'
                # print('sending req \n' + print_str)
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
        dumped_alterations = request.answer_data
        alterations = []
        for dumped_alteration in dumped_alterations:
            alterations.append(Alteration.serialize_from_dump(dumped_alteration))
        for alteration in alterations:
            self.notify_versions_range_with_synchronised_alterations(
                alteration.get_versions_range(),
                self.get_peer_metadata(request.peer, 'database_id')
            )
            self.insert_alteration(alteration)

    def __send_data_to_interface(self):
        s = "Db version: " + str(self.get_last_version())
        return s

    def __process_interface_command(self, command):
        command_words = command.split(' ')
        if command_words[0] == 'show':
            return repr(Alteration.merge(self.get_alterations(VersionsRange(first=0, last=None))).get_changes())
        elif command_words[0] == 'add':
            self.insert_alteration(
                Alteration(
                    {command_words[1]: command_words[2]},
                    VersionsRange(version=self.get_last_version() + 1)
                )
            )
            return 'Yahoo!'
        return 'Undefined command'

    def __register_interface_callbacks(self):
        Interface.register_output_callback('db', self.__send_data_to_interface)
        Interface.register_command_processor_callback('db', self.__process_interface_command)

    def __get_peers_database_working_with(self):
        return self.__networking.get_peers()
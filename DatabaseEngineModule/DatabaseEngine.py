from threading import Timer
import json

from NetworkingModule.NetworkingUsingModule import *


class DatabaseEngine(NetworkingUsingModule):

    def __init__(self, networking, request_processor):
        super().__init__(networking, request_processor, 'database_engine')

        self.__databases = []

        self.register_requests_callbacks()
        self.process()

    def add_database(self, database):
        self.__databases.append(database)

    def process(self):
        update_timeout = 5

        for peer in self.networking.get_peers():
            print('request has been sent')
            self.send_request(peer,  'version_request', 'Give me your db version')

        timer = Timer(update_timeout, self.process)
        timer.start()

    def register_requests_callbacks(self):
        self.register_request_answer_generator(
            'version_request',
            self.database_version_request_answer_generator
        )
        self.register_answer_received_callback(
            'version_request',
            self.database_version_request_answer_received
        )

    def database_version_request_answer_received(self, request):
        new_data = json.JSONDecoder().decode(request.answer_data)
        print(new_data)
        for database_prefix in new_data:
            if new_data[database_prefix]['db_version'] > self.get_database(database_prefix).get_version():
                if new_data[database_prefix]['db_hash'] == self.get_database(database_prefix):
                    print('Branched version detected')
                else:
                    print('New version detected')

    def get_database(self, prefix):
        for database in self.__databases:
            if database.get_prefix() == prefix:
                return database

    def database_version_request_answer_generator(self, request_data):
        message = {}
        for db in self.__databases:
            message[db.get_prefix()] = {
                "db_version": db.get_version(),
                "db_hash": db.get_hash()
            }
        answer = json.JSONEncoder().encode(message)
        return answer
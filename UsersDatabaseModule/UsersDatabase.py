from DatabaseEngineModule.DatabaseEngine import *


class UsersDatabase(DatabaseEngine):

    def __init__(self, networking, requests_processor):
        DatabaseEngine.__init__(self, networking, requests_processor, 'users_database')

    def insert_alteration(self, new_alteration):
        DatabaseEngine.insert_alteration(self, new_alteration)
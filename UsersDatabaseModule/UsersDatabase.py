from DatabaseEngineModule.DatabaseEngine import *


class UsersDatabase(DatabaseEngine):

    def __init__(self, networking, requests_processor):
        DatabaseEngine.__init__(self, networking, requests_processor, 'users_database')

        self.__name = ''

    def insert_alteration(self, new_alteration):
        DatabaseEngine.insert_alteration(self, new_alteration)

    def send_data_to_interface(self):
        if self.is_logged_in():
            return 'Logged as: ' + self.get_name()
        else:
            return 'Not logged in.'

    def process_interface_command(self, command):
        command_words = command.split(' ')
        if command_words[0] == 'register':
            self.__register_as(command_words[1])
        elif command_words[0] == 'login':
            pass
        else:
            return 'Undefined command'

    def __register_as(self, name):
        # if
        pass

    def is_logged_in(self):
        return False

    def get_name(self):
        return self.__name

    def register_interface_callbacks(self):
        Interface.register_output_callback('auth', self.send_data_to_interface)
        Interface.register_command_processor_callback('auth', self.process_interface_command)
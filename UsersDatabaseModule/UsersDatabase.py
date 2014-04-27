from DatabaseEngineModule.DatabaseEngine import *
from UsersDatabaseModule.Cryptography import *


class UsersDatabase(DatabaseEngine):

    def __init__(self, networking, requests_processor):
        DatabaseEngine.__init__(self, networking, requests_processor, 'users_database')

        self.__name = None
        self.__keys = None

    def insert_alteration(self, new_alteration):
        print('New alteration: ' + repr(new_alteration))
        DatabaseEngine.insert_alteration(self, new_alteration)

    def send_data_to_interface(self):
        if self.is_logged_in():
            return 'Logged as: ' + repr(self.get_name())
        else:
            return 'Not logged in.'

    def process_interface_command(self, command):
        command_words = command.split(' ')
        if command_words[0] == 'register':
            return self.__register_as(command_words[1])
        elif command_words[0] == 'login':
            pass
        elif command_words[0] == 'show':
            return self.restore_a_table(VersionsRange(first=0, last=None))
        else:
            return 'Undefined command'

    def __register_as(self, name):
        answer = ''
        if not self.find_in_restored_table(VersionsRange(first=0, last=None), name) is None:
            answer = 'Already registered!'
        else:
            self.__keys = Cryptography.generate_keys()
            new_alteration = Alteration(
                {
                    name: {
                        'connection_data': 'no',
                        'public_key': self.__keys['public_key'],
                        'connection_time': time(),
                        'signature': Cryptography.get_signature('no', self.__keys['private_key'])
                    }
                },
                VersionsRange(version=self.get_last_version())
            )
            self.insert_alteration(new_alteration)
            answer = 'Successfully registered!'
        return answer

    def is_logged_in(self):
        return False

    def get_name(self):
        return self.__name

    def register_interface_callbacks(self):
        Interface.register_output_callback('auth', self.send_data_to_interface)
        Interface.register_command_processor_callback('auth', self.process_interface_command)
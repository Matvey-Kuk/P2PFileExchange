from DatabaseEngineModule.DatabaseEngine import *
from UsersDatabaseModule.Cryptography import *
import json


class UsersDatabase(DatabaseEngine):

    def __init__(self, networking, requests_processor, self_ip_detector):
        super().__init__(networking, requests_processor, 'users_database')
        self.self_ip_detector = self_ip_detector

        self.__name = None
        self.__keys = None
        self.__groups = {}

    def __logout(self):
        self.__name = None
        self.__keys = None
        self.__groups = None

    def insert_alteration(self, new_alteration):
        if self.check_alteration_ligitimity(new_alteration):
            print('New alteration: ' + repr(new_alteration))
            DatabaseEngine.insert_alteration(self, new_alteration)

    def check_alteration_ligitimity(self, alteration):
        result = True
        changes = alteration.get_changes()
        for key in changes:
            if not self.find_in_restored_table(VersionsRange(first=0, last=None), key) is None:
                if not Cryptography.verify_signature(
                        changes[key]['connection_data'] + changes[key]['groups'] + repr(changes[key]['update_data_time']),
                        changes[key]['public_key'],
                        changes[key]['signature']
                ):
                    result = False
        return result

    def get_peers_for_group(self, administrator_name, group_name):
        user_data = self.find_in_restored_table(VersionsRange(first=0, last=None), administrator_name)
        if group_name in user_data['groups']:
            print(user_data['groups'])
            print(type(user_data['groups']))
        return 'Ok'

    def send_data_to_interface(self):
        if not self.__name is None:
            return 'Logged as: ' + repr(self.get_name())
        else:
            return 'Not logged in.'

    def process_interface_command(self, command):
        command_words = command.split(' ')
        if command_words[0] == 'register':
            return self.__register_as(command_words[1])
        elif command_words[0] == 'logout':
            self.__logout()
            return 'Successfully logout.'
        elif command_words[0] == 'show_last_connection_time':
            return self.__get_last_connection_time(command_words[1])
        elif command_words[0] == 'save_keys':
            return self.__save_keys(command_words[1])
        elif command_words[0] == 'load_keys':
            return self.__load_keys(command_words[1])
        elif command_words[0] == 'add_user_to_group':
            self.__add_user_to_group(command_words[1], command_words[2])
            return 'Succeed!'
        elif command_words[0] == 'show_users_in_group':
            return
        elif command_words[0] == 'show_peers_for_group':
            return self.get_peers_for_group(command_words[1], command_words[2])
        elif command_words[0] == 'show_users':
            return " ".join(self.get_authorized_users())
        elif command_words[0] == 'show':
            return repr(self.restore_a_table(VersionsRange(first=0, last=None)))
        else:
            return 'Undefined command'

    def __get_last_connection_time(self, username):
        restored_table = self.restore_a_table(VersionsRange(first=0, last=None))
        return str(restored_table[username]['update_data_time'])

    def get_authorized_users(self):
        users = []
        restored_table = self.restore_a_table(VersionsRange(first=0, last=None))
        for user in restored_table:
            users.append(user)
        return users

    def __save_keys(self, file_path):
        f = open(file_path, "w")
        data = {
            'name': self.__name,
            'keys': self.__keys
        }
        data = json.JSONEncoder().encode(data)
        f.write(data)
        f.close()
        return 'Success.'

    def __load_keys(self, file_path):
        f = open(file_path, "r")
        data = f.read()
        data = json.JSONDecoder().decode(data)
        f.close()
        self.__name = data['name']
        self.__keys = data['keys']
        self.__update_data_in_database()
        return 'Logged in.'

    def __add_user_to_group(self, group_name, user_name):
        if group_name in self.__groups:
            if user_name in group_name:
                return 0
        if not group_name in self.__groups:
            self.__groups[group_name] = []
        self.__groups[group_name].append(user_name)
        self.__update_data_in_database()

    def get_groups(self):
        return json.JSONEncoder().encode(self.__groups)

    def __register_as(self, name):
        answer = ''
        if not self.find_in_restored_table(VersionsRange(first=0, last=None), name) is None:
            answer = 'Already registered!'
        else:
            self.__name = name
            self.__keys = Cryptography.generate_keys()
            self.__update_data_in_database()
            answer = 'Successfully registered!'
        return answer

    def __pack_connection_data(self):
        new_connection_data = {
            'ips': self.self_ip_detector.get_self_ips(),
            'server_port': repr(self.networking.server_port)
        }
        return json.JSONEncoder().encode(new_connection_data)

    def __update_data_in_database(self):
        creation_time = time()
        new_alteration = Alteration(
            {
                self.__name: {
                    'connection_data': self.__pack_connection_data(),
                    'groups': self.get_groups(),
                    'public_key': self.__keys['public_key'],
                    'update_data_time': creation_time,
                    'signature': Cryptography.get_signature(
                        self.__pack_connection_data() + self.get_groups() + repr(creation_time),
                        self.__keys['private_key']
                    )
                }
            },
            VersionsRange(version=self.get_last_version() + 1)
        )
        self.insert_alteration(new_alteration)

    def get_name(self):
        return self.__name

    def register_interface_callbacks(self):
        Interface.register_output_callback('auth', self.send_data_to_interface)
        Interface.register_command_processor_callback('auth', self.process_interface_command)
import hashlib


class Database(object):

    def __init__(self):
        self.__version = 0
        self.__table = {
            'alex': '{"pubkey": "hewjhrkejwhrjhewkr:", "ip":"127.0.0.1", "port":123}',
            'bob': '{"pubkey": "asdasdsdsd:", "ip":"127.0.0.1", "port":12344}',
        }

    def get_version(self):
        return self.__version

    def get_hash(self):
        return hashlib.sha224(str(sorted(self.__table)).encode('utf-8')).hexdigest()

    def get_serialized(self):
        pass

    def merge_update(self, serialized_db, new_version):
        pass

    def merge_branched_same_version(self, serialized_db):
        pass

    def new_record(self, key, value):
        pass

    def edit_record(self, key, value):
        pass

    def get_record(self, key):
        pass
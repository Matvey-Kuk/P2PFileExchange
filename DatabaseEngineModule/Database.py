import hashlib


class Database(object):

    def __init__(self, prefix):
        self.__prefix = prefix
        self.__version = 0
        self.__table = {
            'alex': '{"pubkey": "hewjhrkejwhrjhewkr:", "ip":"127.0.0.1", "port":123}',
            'bob': '{"pubkey": "asdasdsdsd:", "ip":"127.0.0.1", "port":12344}',
        }

        self.__retrospective_max_length = 10
        self.__retrospective_tables = {}

    def get_prefix(self):
        return self.__prefix

    def get_version(self):
        return self.__version

    def get_hash(self, retrospective_version=None):
        if retrospective_version is None:
            return hashlib.sha224(str(sorted(self.__table)).encode('utf-8')).hexdigest()

    def get_serialized(self, retrospective_version=None):
        return repr(self.__table)

    def merge_update(self, serialized_db, new_version):
        pass

    def merge_branched_same_version(self, serialized_db):
        pass

    def new_record(self, key, value):
        self.__dump_retrospective()
        self.__table[key] = value
        self.__version += 1

    def edit_record(self, key, value):
        self.__dump_retrospective()
        self.__table[key] = value
        self.__version += 1

    def get_record(self, key, retrospective_version=None):
        if retrospective_version is None:
            pass

    def __dump_retrospective(self):
        if len(self.__retrospective_tables) > self.__retrospective_max_length:
            oldest_version = None
            for version in self.__retrospective_tables:
                if oldest_version is None:
                    oldest_version = version
                if version < oldest_version:
                    oldest_version = version
            del self.__retrospective_tables[oldest_version]
        self.__retrospective_tables[self.__version] = self.__table.copy()
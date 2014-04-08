import hashlib


class Table(object):
    """Состоит из набора последовательных изменений."""

    def __init__(self, prefix):
        self.__prefix = prefix
        self.__version = 0
        self.__alterations = {}

    def get_prefix(self):
        return self.__prefix

    def get_version(self):
        return self.__version

    def get_hash(self, retrospective_version=None):
        if retrospective_version is None:
            return hashlib.sha224(str(sorted(self.__table)).encode('utf-8')).hexdigest()

    def get_alterations(self, first_version, last_version):
        raise Exception('Method is not written yet')

    def new_alteration(self, key, value):
        raise Exception('Method is not written yet')

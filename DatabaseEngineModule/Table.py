import hashlib

from DatabaseEngineModule.Alteration import Alteration


class Table(object):
    """Состоит из набора последовательных изменений."""

    def __init__(self, prefix):
        self.__prefix = prefix
        self.__version = 0
        self.__alterations = []

        #Используются для разбиения таблицы для нескольких нодов
        self.__lower_limit_of_the_range = None
        self.__upper_limit_of_the_range = None

    def get_prefix(self):
        return self.__prefix

    def get_version(self):
        return self.__version

    def get_hash(self):
        return hashlib.sha224(str(self.merge_rows()).encode('utf-8')).hexdigest()

    def get_alterations(self, first_version, last_version):
        raise Exception('Method is not written yet')

    def new_alteration(self, rows):
        self.__version += 1
        self.__alterations.append(Alteration(version=self.__version, rows=rows))

    def insert_alteration(self, alteration):
        self.__alterations.append(alteration)

    def merge_rows(self, first_version=0, last_version=None):
        result_rows = {}

        if last_version is None:
            last_version = self.__version

        for iterated_version in range(first_version, last_version + 1):
            current_version_alterations = []
            for alteration in self.__alterations:
                if alteration.get_version() == iterated_version:
                    current_version_alterations.append(alteration)
            latest_alteration = None
            for current_version_alteration in current_version_alterations:
                if latest_alteration is None:
                    latest_alteration = current_version_alteration
                else:
                    if latest_alteration.get_creation_time() < current_version_alteration.get_creation_time():
                        latest_alteration = current_version_alteration
            if not latest_alteration is None:
                latest_alteration_rows = latest_alteration.get_rows()
                for key in latest_alteration_rows:
                    result_rows[key] = latest_alteration_rows[key]

        return result_rows
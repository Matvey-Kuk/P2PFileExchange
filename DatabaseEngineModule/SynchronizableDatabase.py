import random

from DatabaseEngineModule.Database import *
from DatabaseEngineModule.VersionsRange import *
from DatabaseEngineModule.ForeignDatabase import *


class SynchronizableDatabase(Database):
    """
    Это база данных, которая умеет синхронизироваться со своими сородичами.
    """

    def __init__(self):
        super().__init__()

        self.__id = hash(random.random())

        self.__foreign_databases = []

    def get_condition(self, versions_range):
        """
        Получить состояние базы в указанном диапазоне версий (хеши).
        """
        self_last_version = self.get_last_version()
        if self_last_version is None:
            self_last_version = 0
        versions_range.concretize_infinity(self_last_version)
        return {
            'hash': self.get_hash(versions_range),
            'id': self.__id,
            'versions_range': versions_range.get_dump()
        }

    def notify_condition(self, condition):
        """
        Сообщить базе о внешней базе и ее состоянии в указанном диапазоне.
        """
        detected_foreign_database = self.__get_foreign_database(condition['id'])
        versions_range_from_condition = VersionsRange(dump=condition['versions_range'])
        if self.get_hash(versions_range_from_condition) == condition['hash']:
            detected_foreign_database.set_versions_range_with_detected_hash_equivalence(versions_range_from_condition)
        else:
            detected_foreign_database.set_versions_range_with_detected_hash_difference(versions_range_from_condition)

    def get_versions_ranges_required_from_another_database(self, database_id):
        """
        Получить, какие состояния требуется узнать у другой базы.
        """
        foreign_database = self.__get_foreign_database(database_id)
        return foreign_database.get_ranges_level_for_binary_search_in_foreign_database()

    def get_versions_ranges_for_required_from_foreign_database_alterations(self, database_id):
        """
        Получить диапазоны необходимых "Шариков"
        """
        foreign_database = self.__get_foreign_database(database_id)
        return foreign_database.get_ranges_with_needed_alterations_in_foreign_database()

    def notify_about_absolete_data(self, versions_range, database_id_with_newer_data):
        """
        Уведомить базу о том, что у нее содержится устарелая информация в диапазоне версий,
        а так же указать, в какой базе доступна более новая информация.
        """
        foreign_database = self.__get_foreign_database(database_id_with_newer_data)
        foreign_database.insert_new_versions_range_with_different_alterations(versions_range)

    def get_id(self):
        return self.__id

    def __get_foreign_database(self, database_id):
        detected_foreign_database = None

        for foreign_database in self.__foreign_databases:
            if foreign_database.get_id() == database_id:
                detected_foreign_database = foreign_database

        if detected_foreign_database is None:
            detected_foreign_database = ForeignDatabase(database_id)

        self.__foreign_databases.append(detected_foreign_database)
        return detected_foreign_database

    def is_alteration_known(self, alteration):
        known = False
        for self_alteration in self.get_alterations(VersionsRange(first=0, last=None)):
            if self_alteration == alteration:
                known = True
        return known
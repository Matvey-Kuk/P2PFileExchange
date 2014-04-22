import random

from DatabaseEngineModule2.Database import *
from DatabaseEngineModule2.VersionsRange import *
from DatabaseEngineModule2.ForeignDatabase import *


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
        versions_range.concretize_infinity(self.get_last_version())
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

    def get_versions_range_required_from_another_database(self, database_id):
        """
        Получить, какие состояния требуется узнать у другой базы.
        """
        foreign_database = self.__get_foreign_database(database_id)
        return foreign_database.get_range_with_detected_hash_differences()

    def notify_about_absolete_data(self, version_first, version_last, database_id_with_newer_data):
        """
        Уведомить базу о том, что у нее содержится устарелая информация в диапазоне версий,
        а так же указать, в какой базе доступна более новая информация.
        """
        raise Exception('Not written yet.')

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
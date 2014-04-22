from DatabaseEngineModule2.VersionsRange import *


class ForeignDatabase(object):
    """
    Класс хранит информацию об удаленной базе данных.
    Используется для поиска в удаленной базе того места, где содержатся неизвестные "шарики".
    """

    def __init__(self, database_id):
        self.__id = database_id

        self.__latest_version = None

        self.__versions_ranges_with_detected_hash_differences = []
        self.__versions_ranges_with_detected_different_alterations = []

    def get_id(self):
        return self.__id

    def set_versions_range_with_detected_hash_difference(self, versions_range):
        if versions_range in self.__versions_ranges_with_detected_hash_differences:
            self.__versions_ranges_with_detected_different_alterations.append(versions_range)
        else:
            self.__versions_ranges_with_detected_hash_differences.append(versions_range)

    def set_versions_range_with_detected_hash_equivalence(self, versions_range):
        for versions_range in self.__versions_ranges_with_detected_hash_differences:
            versions_range = VersionsRange.subtraction(versions_range, versions_range)

    def get_range_with_detected_hash_differences(self):
        if len(self.__versions_ranges_with_detected_hash_differences) > 0:
            return self.__versions_ranges_with_detected_hash_differences[0]
        else:
            return None

    def set_latest_version(self, version):
        raise Exception('Not written yet.')
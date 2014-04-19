

class ForeignDatabase(object):
    """
    Класс хранит информацию об удаленной базе данных.
    Используется для поиска в удаленной базе того места, где содержатся неизвестные "шарики".
    """

    def __init__(self, database_id):
        self.__id = database_id

        self.__latest_version = None

        self.__versions_ranges_with_detected_hash_differences = []

    def get_id(self):
        return self.__id

    def set_versions_range_with_detected_hash_difference(self, version_first, version_last):
        raise Exception('Not written yet.')

    def set_versions_range_with_detected_hash_equivalence(self, version_first, version_last):
        raise Exception('Not written yet.')

    def get_range_with_detected_hash_differences(self):
        raise Exception('Not written yet.')

    def set_latest_version(self, version):
        raise Exception('Not written yet.')
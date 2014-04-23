from DatabaseEngineModule2.VersionsRange import *


class ForeignDatabase(object):
    """
    Класс хранит информацию об удаленной базе данных.
    Используется для поиска в удаленной базе того места, где содержатся неизвестные "шарики".
    """

    def __init__(self, database_id):
        self.__id = database_id

        self.__latest_version = None

        #Глубина, с коророй начнется бинарный поиск новых "шариков". Это "оптимизационная граница".
        self.__binary_search_deep_limit = 100

        """
        Бинарный поиск новых "шариков" осуществляется по уровням.
        Сначала диапазон делится на 2- выше и ниже "оптимизационной границы" - это первый уровень поиска.
        Потом каждый из этих 2-х диапазонов делится еще на 2- это 2-й уровень поиска итд.
        В следующей переменной хранятся {уровень поиска: [диапазоны]}
        """
        self.__versions_ranges_with_detected_hash_differences = {}
        self.__current_search_level = 0

        self.__detected_ranges_with_different_alterations = []

    def get_id(self):
        return self.__id

    def set_versions_range_with_detected_hash_difference(self, versions_range):
        #Если первая итерация поиска
        if self.__current_search_level == 0:
            self.__current_search_level = 1
            #Проверяем, нужно ли нам применить "оптимизационную границу"
            if versions_range.get_last() > self.__binary_search_deep_limit:
                self.__versions_ranges_with_detected_hash_differences[1] = [
                    VersionsRange(
                        first=0,
                        last=versions_range.get_last() - self.__binary_search_deep_limit
                    ),
                    VersionsRange(
                        first=versions_range.get_last() - self.__binary_search_deep_limit + 1,
                        last=versions_range.get_last()
                    )
                ]
            else:
                self.__versions_ranges_with_detected_hash_differences[self.__current_search_level] = \
                    VersionsRange.divide_range(versions_range)
        else:
            self.__remove_versions_range_from_search_level(versions_range, self.__current_search_level)

            #Проверяем, не является ли диапазон неразбиваемым:
            if versions_range.get_size() == 1:
                if not versions_range in self.__detected_ranges_with_different_alterations:
                    self.__detected_ranges_with_different_alterations.append(versions_range)
            else:
                #Бьем его и добавляем на следующий
                self.__versions_ranges_with_detected_hash_differences[self.__current_search_level] += \
                    VersionsRange.divide_range(versions_range)

            #Проверяем переход на следующий уровень
            if len(self.__versions_ranges_with_detected_hash_differences[self.__current_search_level]) == 0:
                self.__current_search_level += 1

            if not self.__current_search_level in self.__versions_ranges_with_detected_hash_differences:
                self.__current_search_level = 0

    def set_versions_range_with_detected_hash_equivalence(self, versions_range):
        for search_level in self.__versions_ranges_with_detected_hash_differences:
            if versions_range in self.__versions_ranges_with_detected_hash_differences[search_level]:
                self.__versions_ranges_with_detected_hash_differences[search_level].remove(versions_range)

    def __remove_versions_range_from_search_level(self, versions_range, search_level):
        new_versions_ranges_in_current_level = []

        for versions_range_in_current_level in \
                self.__versions_ranges_with_detected_hash_differences[search_level]:
            if not versions_range == versions_range_in_current_level:
                new_versions_ranges_in_current_level.append(versions_range_in_current_level)

        self.__versions_ranges_with_detected_hash_differences[search_level] = \
            new_versions_ranges_in_current_level

    def get_ranges_level_for_binary_search_in_foreign_database(self):
        """
        Получаем все диапазоны на текущем уровне поиска, в которых обнаружено несоответствие хешей.
        """
        if self.__current_search_level == 0:
            return [VersionsRange(first=0, last=None)]
        else:
            return self.__versions_ranges_with_detected_hash_differences[self.__current_search_level]

    def get_ranges_with_needed_alterations_in_foreign_database(self):
        return self.__detected_ranges_with_different_alterations

    def set_latest_version(self, version):
        raise Exception('Not written yet.')
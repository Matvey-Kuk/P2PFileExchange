from DatabaseEngineModule2.VersionsRange import *


class Database(object):
    """
    База данных, работает с "шариками".
    """

    def __init__(self):
        self.__alterations = []

    def insert_alteration(self, new_alteration):
        eq_alteration_detected = False
        for alteration in self.__alterations:
            if alteration == new_alteration:
                eq_alteration_detected = True
        if not eq_alteration_detected:
            self.__alterations.append(new_alteration)

    def get_alterations(self, versions_range):
        needed_alterations = []
        for alteration in self.__alterations:
            if versions_range.includes(alteration.get_versions_range()):
                needed_alterations.append(alteration)
        return needed_alterations

    def restore_a_table(self, version_first=0, version_last=None):
        raise Exception('Not written yet.')

    def find_in_restored_table(self, key):
        raise Exception('Not written yet.')

    def get_hash(self, version_first=0, version_last=None):
        raise Exception('Not written yet.')
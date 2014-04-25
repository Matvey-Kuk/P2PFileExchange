import hashlib

from DatabaseEngineModule.VersionsRange import *
from DatabaseEngineModule.Alteration import *


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
            print('----' + repr(new_alteration))
            self.__alterations.append(new_alteration)

    def get_last_version(self):
        last_version = None
        for alteration in self.__alterations:
            if last_version is None:
                last_version = alteration.get_versions_range().get_last()
            if last_version < alteration.get_versions_range().get_last():
                last_version = alteration.get_versions_range().get_last()
        if last_version is None:
            last_version = 0
        return last_version

    def get_alterations(self, versions_range):
        needed_alterations = []
        for alteration in self.__alterations:
            if versions_range.includes(alteration.get_versions_range()):
                needed_alterations.append(alteration)
        return needed_alterations

    def restore_a_table(self, versions_range):
        needed_alterations = self.get_alterations(versions_range)
        merged = Alteration.merge(needed_alterations)
        return merged.get_changes()

    def find_in_restored_table(self, versions_range, key):
        return self.restore_a_table(versions_range)[key]

    def get_hash(self, versions_range):
        return hashlib.sha224(str(self.restore_a_table(versions_range)).encode('utf-8')).hexdigest()

    def __repr__(self):
        string = ''
        sorted_alterations = sorted(self.__alterations, key=lambda alteration: alteration.get_versions_range())
        for alteration in sorted_alterations:
            string += '\n' + repr(alteration)
        return string
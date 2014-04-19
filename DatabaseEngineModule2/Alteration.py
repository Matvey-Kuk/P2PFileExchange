from time import time


class Alteration(object):
    """
    Изменение- единица, которой оперирует база данных. Тот самый "шарик".
    """

    def __init__(self, changes, versions_range):
        self.__changes = changes
        self.__versions_range = versions_range
        self.__creation_time = time()

    def get_versions_range(self):
        return self.__versions_range

    def get_changes(self):
        return self.__changes

    def get_creation_time(self):
        return self.__creation_time

    @staticmethod
    def merge(alterations):
        result_changes = {}
        for alteration in alterations:
            pass
from time import time

from DatabaseEngineModule2.VersionsRange import *


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
        result_changes_with_versions_and_times = {}
        for alteration in alterations:
            changes = alteration.get_changes()
            for key in changes:
                write_ready = False
                if not key in result_changes_with_versions_and_times:
                    write_ready = True
                if key in result_changes_with_versions_and_times:
                    if result_changes_with_versions_and_times[key]['version'] < alteration.get_versions_range():
                        write_ready = True
                    if result_changes_with_versions_and_times[key]['version'] == alteration.get_versions_range():
                        if result_changes_with_versions_and_times[key]['time'] < alteration.get_creation_time():
                            write_ready = True
                if write_ready:
                    result_changes_with_versions_and_times[key] = {
                        'value': changes[key],
                        'version': alteration.get_versions_range(),
                        'time': alteration.get_creation_time()
                    }
        result_changes = {}
        for key in result_changes_with_versions_and_times:
            result_changes[key] = result_changes_with_versions_and_times[key]['value']

        return Alteration(result_changes,VersionsRange(version=0))
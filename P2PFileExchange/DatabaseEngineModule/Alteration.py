from time import time

from DatabaseEngineModule.VersionsRange import *


class Alteration(object):
    """
    Изменение- единица, которой оперирует база данных. Тот самый "шарик".
    """

    def __init__(self, changes, versions_range, **kwargs):
        self.__changes = changes
        self.__versions_range = versions_range
        if 'creation_time' in kwargs:
            self.__creation_time = kwargs['creation_time']
        else:
            self.__creation_time = time()

    def get_versions_range(self):
        return self.__versions_range

    def get_changes(self):
        return self.__changes

    def get_creation_time(self):
        return self.__creation_time

    def __eq__(self, other):
        return self.__changes == other.get_changes() and self.__versions_range == other.get_versions_range() and \
               self.__creation_time == other.get_creation_time()

    @staticmethod
    def merge(alterations):
        result_changes_with_versions_and_times = {}
        versions_ranges = []
        for alteration in alterations:
            changes = alteration.get_changes()
            versions_ranges.append(alteration.get_versions_range())
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

        return Alteration(result_changes, VersionsRange.merge(versions_ranges))

    def __eq__(self, other):
        self_changes = self.get_changes()
        other_changes = other.get_changes()
        changes_eq = True
        for key_s in self_changes:
            if not key_s in other_changes:
                changes_eq = False
            elif not self_changes[key_s] == other_changes[key_s]:
                changes_eq = False
        for key_o in other_changes:
            if not key_o in self_changes:
                changes_eq = False
            elif not self_changes[key_o] == other_changes[key_o]:
                changes_eq = False
        return changes_eq and self.get_versions_range() == other.get_versions_range()

    def __repr__(self):
        return "Changes: " + repr(self.__changes) + ' Versions range: ' + repr(self.__versions_range) + \
               ' Creation time: ' + repr(self.__creation_time)

    def get_dump(self):
        return {
            'changes': self.__changes,
            'versions_range': self.__versions_range.get_dump(),
            'creation_time': self.__creation_time
        }

    @staticmethod
    def serialize_from_dump(alteration_dump):
        return Alteration(
            alteration_dump['changes'],
            VersionsRange(dump=alteration_dump['versions_range']),
            creation_time=alteration_dump['creation_time']
        )
import unittest

from DatabaseEngineModule2.SynchronizableDatabase import *


class TestSynchronizableDatabase(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_versions_range_required_from_another_database(self):
        database_a = SynchronizableDatabase()
        database_a.insert_alteration(Alteration({'a': 1}, VersionsRange(version=4)))
        database_a.insert_alteration(Alteration({'a': 2}, VersionsRange(version=6)))

        database_b = SynchronizableDatabase()
        database_b.insert_alteration(Alteration({'a': 1}, VersionsRange(version=4)))

        database_b.notify_condition(database_a.get_condition(VersionsRange(first=4, last=None)))

        self.assertEqual(
            database_b.get_versions_range_required_from_another_database(database_a.get_id()),
            VersionsRange(first=4, last=6)
        )
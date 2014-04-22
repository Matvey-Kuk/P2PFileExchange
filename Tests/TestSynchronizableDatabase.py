import unittest

from DatabaseEngineModule2.SynchronizableDatabase import *


class TestSynchronizableDatabase(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_versions_range_required_from_another_database(self):
        database_a = SynchronizableDatabase()
        database_a.insert_alteration(Alteration({'a': 1}, VersionsRange(version=4)))

        database_b = SynchronizableDatabase()
        database_b.insert_alteration(Alteration({'a': 1}, VersionsRange(version=4)))

        #Проверим, что b от a хочет весь диапазон

        database_b.notify_condition(database_a.get_condition(VersionsRange(first=0, last=None)))

        self.assertEqual(
            database_b.get_versions_ranges_required_from_another_database(database_a.get_id()),
            [VersionsRange(first=0, last=None)]
        )

        #Теперь в базе "a" пополнение и "b" хочет от нее ограниченный диапазон
        database_a.insert_alteration(Alteration({'a': 2}, VersionsRange(version=6)))

        database_b.notify_condition(database_a.get_condition(VersionsRange(first=0, last=None)))

        self.assertEqual(
            database_b.get_versions_ranges_required_from_another_database(database_a.get_id()),
            [VersionsRange(first=0, last=3), VersionsRange(first=4, last=6)]
        )

        #Уведомим "b" о хешах в новых диапазонах:
        database_b.notify_condition(database_a.get_condition(VersionsRange(first=0, last=3)))
        database_b.notify_condition(database_a.get_condition(VersionsRange(first=4, last=6)))

        #Проверим, что нужно базе опять:
        self.assertEqual(
            database_b.get_versions_ranges_required_from_another_database(database_a.get_id()),
            [VersionsRange(first=4, last=5), VersionsRange(version=6)]
        )
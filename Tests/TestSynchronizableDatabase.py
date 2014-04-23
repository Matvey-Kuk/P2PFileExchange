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

    def test_get_different_alterations(self):
        database_a = SynchronizableDatabase()
        database_a.insert_alteration(Alteration({'a': 1}, VersionsRange(version=1)))
        database_a.insert_alteration(Alteration({'a': 2}, VersionsRange(version=2)))
        database_a.insert_alteration(Alteration({'c': 1}, VersionsRange(version=2)))
        database_a.insert_alteration(Alteration({'a': 3}, VersionsRange(version=3)))

        database_b = SynchronizableDatabase()
        database_b.insert_alteration(Alteration({'a': 1}, VersionsRange(version=1)))
        database_b.insert_alteration(Alteration({'a': 2}, VersionsRange(version=2)))
        database_b.insert_alteration(Alteration({'a': 3}, VersionsRange(version=3)))

        self.define_different_alterations(database_a, database_b, 40)
        self.assertEqual(
            database_b.get_versions_ranges_for_required_from_foreign_database_alterations(database_a.get_id()),
            [VersionsRange(version=2)]
        )
        self.assertEqual(
            database_a.get_versions_ranges_for_required_from_foreign_database_alterations(database_b.get_id()),
            [VersionsRange(version=2)]
        )

    def sync_databases(self, database_a, database_b):
        required_versions_ranges = database_b.get_versions_ranges_required_from_another_database(database_a.get_id())
        for required_versions_range in required_versions_ranges:
            database_b.notify_condition(database_a.get_condition(required_versions_range))

    def define_different_alterations(self, database_a, database_b, iterations):
        for i in range(0, iterations):
            self.sync_databases(database_a, database_b)
            self.sync_databases(database_b, database_a)
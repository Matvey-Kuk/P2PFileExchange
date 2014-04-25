import unittest

from DatabaseEngineModule.Database import *
from DatabaseEngineModule.Alteration import *


class TestDatabase(unittest.TestCase):

    def setUp(self):
        pass

    def test_insert_get_alterations(self):
        database = Database()

        #Тестируем отсечение дубляжа
        database.insert_alteration(Alteration({}, VersionsRange(first=2, last=5), creation_time=1234))
        database.insert_alteration(Alteration({}, VersionsRange(first=2, last=5), creation_time=1234))

        database.insert_alteration(Alteration({}, VersionsRange(first=3, last=20)))

        alterations = database.get_alterations(VersionsRange(first=1, last=10))

        self.assertTrue(len(alterations) == 1)
        self.assertEqual(alterations[0].get_versions_range(), VersionsRange(first=2, last=5))

    def test_restore_a_table(self):
        database = Database()
        database.insert_alteration(Alteration({'a': 1}, VersionsRange(version=0)))
        database.insert_alteration(Alteration({'a': 2}, VersionsRange(version=1)))
        database.insert_alteration(Alteration({'a': 3}, VersionsRange(version=2)))
        database.insert_alteration(Alteration({'b': 1}, VersionsRange(version=3)))
        restored_table = database.restore_a_table(VersionsRange(first=0, last=database.get_last_version()))
        self.assertEqual(restored_table, {
            'a': 3,
            'b': 1
        })
        self.assertEqual(
            database.find_in_restored_table(VersionsRange(first=0, last=database.get_last_version()), 'a'),
            3
        )

    def test_get_hash(self):
        database_a = Database()
        database_a.insert_alteration(Alteration({'a': 1}, VersionsRange(version=0)))

        database_b = Database()
        database_b.insert_alteration(Alteration({'a': 1}, VersionsRange(version=0)))

        self.assertEqual(
            database_a.get_hash(VersionsRange(first=0, last=database_a.get_last_version())),
            database_b.get_hash(VersionsRange(first=0, last=database_b.get_last_version())),
        )

        database_a.insert_alteration(Alteration({'b': 1}, VersionsRange(version=1)))

        self.assertNotEqual(
            database_a.get_hash(VersionsRange(first=0, last=database_a.get_last_version())),
            database_b.get_hash(VersionsRange(first=0, last=database_b.get_last_version())),
        )

        database_b.insert_alteration(Alteration({'b': 1}, VersionsRange(version=1)))

        self.assertEqual(
            database_a.get_hash(VersionsRange(first=0, last=database_a.get_last_version())),
            database_b.get_hash(VersionsRange(first=0, last=database_b.get_last_version())),
        )

        database_a.insert_alteration(
            Alteration(
                {
                    'a': '1',
                    'b': '2',
                    'c': '3'
                },
                VersionsRange(version=2)
            )
        )
        database_b.insert_alteration(
            Alteration(
                {
                    'b': '2',
                    'a': '1',
                    'c': '3'
                },
                VersionsRange(version=2)
            )
        )
        self.assertEqual(
            database_a.get_hash(VersionsRange(first=0, last=database_a.get_last_version())),
            database_b.get_hash(VersionsRange(first=0, last=database_b.get_last_version())),
        )
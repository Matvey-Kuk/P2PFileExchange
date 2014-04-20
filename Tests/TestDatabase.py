import unittest

from DatabaseEngineModule2.Database import *
from DatabaseEngineModule2.Alteration import *


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
import unittest

from DatabaseEngineModule2.SynchronizableDatabase import *


class TestSynchronizableDatabase(unittest.TestCase):

    def setUp(self):
        pass

    def test_conditions_exchange(self):
        database_a = SynchronizableDatabase()
        database_b = SynchronizableDatabase()

        print(database_a.get_condition(VersionsRange(first=0, last=None)))
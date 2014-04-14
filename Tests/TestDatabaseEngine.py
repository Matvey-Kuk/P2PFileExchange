import unittest
from unittest.mock import Mock

from DatabaseEngineModule.Table import *


class TestDatabaseEngine(unittest.TestCase):

    def setUp(self):
        pass

    def test_hashes(self):
        table_a = Table('test_table')
        table_b = Table('test_table')
        self.assertEqual(table_a.get_hash(), table_b.get_hash())

        table_a.new_alteration('some_key', 'some_value')
        table_b.new_alteration('some_key', 'some_value')
        self.assertEqual(table_a.get_hash(), table_b.get_hash())

        table_a.new_alteration('some_key', 'some_value')
        table_b.new_alteration('some_key', 'another_value')
        self.assertNotEqual(table_a.get_hash(), table_b.get_hash())
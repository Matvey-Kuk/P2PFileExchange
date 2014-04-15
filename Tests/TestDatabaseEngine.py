import unittest
from unittest.mock import Mock

from DatabaseEngineModule.Table import *


class TestDatabaseEngine(unittest.TestCase):

    def setUp(self):
        pass

    def test_merge_rows(self):
        table = Table('test_table')
        table.new_alteration({'1': 'a'})
        self.assertEqual(table.merge_rows()['1'], 'a')

        table.new_alteration({'1': 'b'})
        table.new_alteration({'1': 'c'})
        table.new_alteration({'1': 'd'})
        self.assertEqual(table.merge_rows()['1'], 'd')

        table.new_alteration({'2': 'local_alteration'})
        foreign_alteration = Alteration(version=table.get_version(), rows={'2': 'foreign_value'})
        table.insert_alteration(foreign_alteration)
        self.assertEqual(table.merge_rows()['2'], 'foreign_value')

    def test_hashes(self):
        table_a = Table('test_table')
        table_b = Table('test_table')
        self.assertEqual(table_a.get_hash(), table_b.get_hash())

        table_a.new_alteration({'some_key': 'some_value'})
        table_b.new_alteration({'some_key': 'some_value'})
        self.assertEqual(table_a.get_hash(), table_b.get_hash())

        table_a.new_alteration({'some_key': 'some_value'})
        table_b.new_alteration({'some_key': 'another_value'})
        self.assertNotEqual(table_a.get_hash(), table_b.get_hash())

        table_a.new_alteration({'some_key': 'some_value'})
        table_b.new_alteration({'some_key': 'some_value'})
        self.assertEqual(table_a.get_hash(), table_b.get_hash())
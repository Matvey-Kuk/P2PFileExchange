import unittest
from unittest.mock import Mock

from DatabaseEngineModule.Table import *
from DatabaseEngineModule.Database import *


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

    # def test_dump_and_returning(self):
    #     table_a = Table('test_table')
    #     table_a.new_alteration({'some_key': 'some_value'})
    #     print(table_a.get_string_representation())

    def test_tables_synchronization(self):
        database_a = Database()
        database_b = Database()

        database_a.add_table(Table('table_for_sync'))
        database_b.add_table(Table('table_for_sync'))

        self.assertEqual(
            database_a.get_table('table_for_sync').get_version(),
            database_b.get_table('table_for_sync').get_version()
        )

        database_a.get_table('table_for_sync').new_alteration({'key': 'value'})

        database_b.notice_foreign_database_condition(database_a.get_condition())
        database_a.notice_foreign_database_condition(database_b.get_condition())

        
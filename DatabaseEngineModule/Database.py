import json
from threading import Timer
import random


class Database(object):
    """Реализует всю поддержку таблиц кроме сетевой."""

    def __init__(self):
        self.__tables = []
        self.__unique_key = random.random()

        self.__required_newer_alterations = []
        self.__required_branched_alterations = []

    def add_table(self, table):
        self.__tables.append(table)

    def get_table(self, prefix):
        for table in self.__tables:
            if table.get_prefix() == prefix:
                return table
        return None

    def get_condition(self):
        tables_conditions = []
        for table in self.__tables:
            tables_conditions.append(
                {
                    'prefix': table.get_prefix(),
                    'version': table.get_version(),
                    'hash': table.get_hash(),
                    'lower_limit_of_the_range': table.get_lower_limit_of_the_range(),
                    'upper_limit_of_the_range': table.get_upper_limit_of_the_range()
                }
            )
        result = {
            'tables_conditions': tables_conditions,
            'unique_key': self.__unique_key
        }
        return result

    def notice_foreign_database_condition(self, condition):
        for table_condition in condition['tables_conditions']:
            self_table = self.get_table(table_condition['prefix'])
            if table_condition['version'] == self_table.get_version():
                if table_condition['hash'] != self_table.get_hash():
                    raise Exception('Branch detected')
            else:
                if table_condition['version'] > self_table.get_version():
                    self.__required_newer_alterations.append({
                        'unique_db_key': condition['unique_key'],
                        'table_prefix': table_condition['prefix'],
                        'from_version': table_condition['version'],
                        'to_version': self.get_table(table_condition['prefix']).get_version()
                    })

    def check_if_required_alterations_from_foreign_db(self, db_unique_key):
        required_alterations = {}
        for required_newer_alteration in self.__required_newer_alterations:
            if required_newer_alteration['unique_db_key'] == db_unique_key:
               print(required_newer_alteration)
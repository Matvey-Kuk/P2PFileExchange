

class Database(object):
    """
    База данных, работает с "шариками".
    """

    def __init__(self):
        raise Exception('Not written yet.')

    def insert_alteration(self, alteration):
        raise Exception('Not written yet.')

    def get_alterations(self, version_first, version_last):
        raise Exception('Not written yet.')

    def restore_a_table(self, version_first=0, version_last=None):
        raise Exception('Not written yet.')

    def find_in_restored_table(self, key):
        raise Exception('Not written yet.')

    def get_hash(self, version_first=0, version_last=None):
        raise Exception('Not written yet.')


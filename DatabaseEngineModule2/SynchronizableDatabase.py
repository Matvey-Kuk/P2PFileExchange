from DatabaseEngineModule2.Database import *


class SynchronizableDatabase(Database):
    """
    Это база данных, которая умеет синхронизироваться со своими сородичами.
    """

    def __init__(self):
        super().__init__()

        self.id = None

    def get_condition(self, version_first=0, version_last=None):
        raise Exception('Not written yet.')

    def notify_condition(self, condition):
        """
        """
        raise Exception('Not written yet.')

    def get_needed_versions_conditions(self, database_id):
        raise Exception('Not written yet.')
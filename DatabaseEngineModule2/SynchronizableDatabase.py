from DatabaseEngineModule2.Database import *


class SynchronizableDatabase(Database):
    """
    Это база данных, которая умеет синхронизироваться со своими сородичами.
    """

    def __init__(self):
        super().__init__()

        self.id = None

    def get_condition(self, version_first=0, version_last=None):
        """
        Получить состояние базы в указанном диапазоне версий (хеши).
        """
        raise Exception('Not written yet.')

    def notify_condition(self, condition):
        """
        Сообщить базе о внешней базе и ее состоянии в указанном диапазоне.
        """
        raise Exception('Not written yet.')
    def get_information_for_foreign_database(self, database_id):
        """
        Узнать, какую информацию требуется передать внешней базе.
        """
        raise Exception('Not written yet.')

    def notify_about_absolete_data(self, version_first, version_last, database_id_with_newer_data):
        """
        Уведомить базу о том, что у нее содержится устарелая информация в диапазоне версий,
        а так же указать, в какой базе доступна более новая информация.
        """
        raise Exception('Not written yet.')
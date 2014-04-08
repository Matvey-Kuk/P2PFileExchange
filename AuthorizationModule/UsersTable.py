from DatabaseEngineModule.Table import *


class UsersTable(Table):
    """Добавляет базе данных методы, которые нужны для хранения пользователей"""

    def __init__(self):
        super().__init__('users_table')
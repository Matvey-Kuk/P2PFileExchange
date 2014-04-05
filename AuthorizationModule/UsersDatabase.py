from DatabaseEngineModule.Database import *


class UsersDatabase(Database):
    """Добавляет базе данных методы, которые нужны для хранения пользователей"""

    def __init__(self):
        super().__init__()
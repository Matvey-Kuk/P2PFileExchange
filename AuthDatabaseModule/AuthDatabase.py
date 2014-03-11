

from NetworkingModule.NetworkingUsingModule import *


class AuthDataBase(NetworkingUsingModule):
    """Модуль распределенной базы данных пользователей"""
    def __init__(self, networking, request_processor):
        super().__init__(networking, request_processor, 'auth_database')
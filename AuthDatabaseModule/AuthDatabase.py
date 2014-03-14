<<<<<<< HEAD
from NetworkingModule.NetworkingUsingModule import *
from threading import Timer
from time import time

class AuthDataBase(NetworkingUsingModule):
    """Модуль распределенной базы данных пользователей"""
    def __init__(self, networking, request_processor):
        super().__init__(networking, request_processor, 'auth_database')
        self.networking=networking
        self.process()
    def process(self):
        super().process()
        update_timeout=1

        timer = Timer(update_timeout, self.process)
        timer.start()

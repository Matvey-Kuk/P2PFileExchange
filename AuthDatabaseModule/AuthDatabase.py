from NetworkingModule.NetworkingUsingModule import *
from threading import Timer
from time import time

class AuthDataBase(NetworkingUsingModule):
    """Модуль распределенной базы данных пользователей"""
    def __init__(self,networking):
        self.prefix="AuDB"
        super().__init__(networking,self.prefix)
        self.networking=networking
        self.process()
    def process(self):
        super().process()
        update_timeout=1




        timer = Timer(update_timeout, self.process)
        timer.start()


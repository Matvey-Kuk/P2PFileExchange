from NetworkingModule.NetworkingUsingModule import *
from threading import Timer
from CryptoModule.rsa import *
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
        self.register_callbacks_for_requests()

        timer = Timer(update_timeout, self.process)
        timer.start()

    def register_callbacks_for_requests(self):
        self.register_request_answer_generator('server_port', self.server_port_request_answer)
        self.register_answer_received_callback('server_port', self.server_port_answer_received)
        self.register_request_answer_generator('peers_request', self.peer_request_answer)
        self.register_answer_received_callback('peers_request', self.peer_request_answer_received)

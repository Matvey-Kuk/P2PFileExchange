from NetworkingModule.NetworkingUsingModule import *
from threading import Timer
from CryptoModule.rsa import *
from time import time


class AuthDataBase(NetworkingUsingModule):
    """Модуль распределенной базы данных пользователей"""

    def __init__(self, networking, request_processor):
        super().__init__(networking, request_processor, 'auth_database')
        self.register_callbacks_for_requests()
        self.process()

    def process(self):
        super().process()
        update_timeout = 1

        for peer in self.networking.get_peers():
            if self.get_peer_metadata(peer, 'some_request') is None:
                request = self.send_request(peer, 'some_request', 'Hello!')
                self.set_peer_metadata(peer, 'some_request', request)

        timer = Timer(update_timeout, self.process)
        timer.start()

    def register_callbacks_for_requests(self):
        self.register_request_answer_generator('some_request', self.some_request_answer_generator)
        self.register_answer_received_callback('some_request', self.some_request_answer_received)

    def some_request_answer_generator(self, question_data):
        return "answer!"

    def some_request_answer_received(self, request):
        print("Answer received:" + request.answer_data)
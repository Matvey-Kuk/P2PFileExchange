from threading import Timer
from time import time
from CryptoModule.rsa import *

from NetworkingModule.NetworkingUsingModule import *


class AuthDataBase(NetworkingUsingModule):
    """Модуль распределенной базы данных пользователей"""

    def __init__(self, networking, request_processor, nick_name):
        super().__init__(networking, request_processor, 'auth_database')
        self.register_callbacks_for_requests()
        my_name=nick_name
        if my_name is None:
            my_name = "Alex"
        print("Nick name: " + my_name)
        # (pubkey, privkey) = rsa.newkeys(512)

        # for peer in self.networking.get_peers():
            # request=self.send_request(peer,'')
        self.process()

    def process(self):
        super().process()
        update_timeout = 1

        for peer in self.networking.get_peers():
            if self.get_peer_metadata(peer, 'verification_request') is None:
                request = self.send_request(peer, 'verification_request', 'Hello! Ti kto takoy?')
                self.set_peer_metadata(peer, 'verification_request', request)

        timer = Timer(update_timeout, self.process)
        timer.start()

    def register_callbacks_for_requests(self):
        self.register_request_answer_generator('welcome', self.welcome_request_answer_generator)
        self.register_answer_received_callback('welcome', self.welcome_request_answer_received)

        self.register_request_answer_generator('verification_request', self.verification_request_answer_generator)
        self.register_answer_received_callback('verification_request', self.verification_request_answer_received)

    def welcome_request_answer_generator(self, question_data):
        return "welcome"

    def welcome_request_answer_received(self, request):
        return "Hello!"

    def verification_request_answer_generator(self, question_data):
        return "answer!"

    def verification_request_answer_received(self, request):
        print("Answer received:" + request.answer_data)
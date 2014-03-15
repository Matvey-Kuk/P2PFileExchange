from threading import Timer
from time import time
import rsa

from NetworkingModule.NetworkingUsingModule import *


class AuthDataBase(NetworkingUsingModule):
    """Модуль распределенной базы данных пользователей"""

    def __init__(self, networking, request_processor, nick_name):
        super().__init__(networking, request_processor, 'auth_database')
        self.register_callbacks_for_requests()
        random_msg=[]
        my_name=nick_name
        if my_name is None:
            my_name = "Alex"
        print("Nick name: " + my_name)
        (pubkey, privkey) = rsa.newkeys(256)

        welcome_data={'nick':my_name,'pubkey':pubkey}
        for peer in self.networking.get_peers():
            print("Request connect me into p2p network")
            welcome_request=self.send_request(peer,'welcome',welcome_data)

        self.process()

    def process(self):
        super().process()
        update_timeout = 1

        for peer in self.networking.get_peers():
            if self.get_peer_metadata(peer, 'welcome') is None:
                request = self.send_request(peer, 'welcome', 'Hello! Ti kto takoy?')
                self.set_peer_metadata(peer, 'welcome', request)

        timer = Timer(update_timeout, self.process)
        timer.start()

    def register_callbacks_for_requests(self):
        self.register_request_answer_generator('welcome', self.welcome_request_answer_generator)
        self.register_answer_received_callback('welcome', self.welcome_request_answer_received)

        self.register_request_answer_generator('verification_request', self.verification_request_answer_generator)
        self.register_answer_received_callback('verification_request', self.verification_request_answer_received)

    def welcome_request_answer_generator(self, ver_data):
        """Генерация шифрованного сообщения и передача для верификации"""
        print("User "+ver_data['nick']+" request conection")
        random_msg = rsa.randnum.read_random_bits(128)
        crypto = rsa.encrypt(random_msg,ver_data['pubkey'])
        answer_data=ver_data.update({'crypto_msg':crypto})
        return answer_data

    def welcome_request_answer_received(self, request_data):
        """Прием зашифрованного сообщения, отправка запроса на проверку для верификации"""
        print("Received crypto message")
        reseive_msg = rsa.decrypt(request_data['crypto_msg'], privkey)
        verif_msg={'nick':request_data['nick'],'pubkey':request_data['pubkey'],'decrypt_msg':reseive_msg}
        ver_request=self.send_request(peer,'verification_request', verif_msg)

    def welcome_request_answer_received(self, request):
        return "Hello!"

    def verification_request_answer_generator(self, verif_msg):
        """Проверка расшифрованного сообщения"""
        if random_msg == verif_msg['decrypt_msg']:
            self.users_list.append=({'nick':verif_msg['nick'],'pubkey':ver_msg['pubkey']})
            print("User "+verif_msg['nick'] +"is authenticated")
            return "Welcome to p2p world!!"
        else:
            print("User "+verif_msg['nick']+"is not authenticated")
            return "Authentication error!!"

    def verification_request_answer_received(self, request):
        print(request)

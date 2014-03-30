import rsa

from NetworkingModule.NetworkingUsingModule import *


class AuthDataBase(NetworkingUsingModule):
    """Модуль распределенной базы данных пользователей"""

    def __init__(self, networking, request_processor, nick_name):
        super().__init__(networking, request_processor, 'auth_database')
        self.register_callbacks_for_requests()
        self.random_msg = []
        self.my_name = nick_name
        self.users_list = ['nick', 'pubkey']
        if self.my_name is None:
            self.my_name = "Alex"
        print("Auth_module: Nick name: " + self.my_name)
        (self.pubkey, self.privkey) = rsa.newkeys(256)
        # msg="Hello my friend"
        # cr=rsa.encrypt(msg, self.pubkey)
        # msg2=rsa.decrypt(cr, self.privkey)
        welcome_data = {'nick': self.my_name, 'pubkey_n': self.pubkey.n, 'pubkey_e': self.pubkey.e}
        for peer in self.networking.get_peers():
            print("Auth_module: Request connect me into p2p network")
            welcome_request = self.send_request(peer, 'welcome', welcome_data)
        # self.process()
    """
    def process(self):
        super().process()
        update_timeout = 1

        for peer in self.networking.get_peers():
            if self.get_peer_metadata(peer, 'welcome') is None:
                request = self.send_request(peer, 'welcome', None)
                self.set_peer_metadata(peer, 'welcome', request)

        timer = Timer(update_timeout, self.process)
        timer.start()
    """

    def register_callbacks_for_requests(self):
        self.register_request_answer_generator('welcome', self.welcome_request_answer_generator)
        self.register_answer_received_callback('welcome', self.welcome_request_answer_received)

        self.register_request_answer_generator('verification_request', self.verification_request_answer_generator)
        self.register_answer_received_callback('verification_request', self.verification_request_answer_received)

        self.register_request_answer_generator('auth_request', self.auth_request_answer_generator)
        self.register_answer_received_callback('auth_request', self.auth_request_answer_received)

    def welcome_request_answer_generator(self, ver_data):
        """Генерация шифрованного сообщения и передача для верификации"""
        print("Auth_module: User ", ver_data['nick'], " request connection")
        self.random_msg = rsa.randnum.read_random_bits(128)
        Pub = rsa.PublicKey(ver_data['pubkey_n'], ver_data['pubkey_e'])
        crypto = rsa.encrypt(self.random_msg, Pub)
        i = 0
        crypto_mas = []
        while i < len(crypto):
            crypto_mas.append(crypto[i])
            i = i+1
        # print(ver_data)
        # answer_data=ver_data.update({'crypto_msg':crypto})
        answer_data = {'nick': ver_data['nick'],
                       'pubkey_n': ver_data['pubkey_n'],
                       'pubkey_e': ver_data['pubkey_e'],
                       'crypto_msg': crypto_mas}
        # print(answer_data)
        for peer in self.networking.get_peers():
            print('Ok')
            self.send_request(peer,  'verification_request', answer_data)


    def welcome_request_answer_received(self, request):
        print("Auth_module: User received my authentication data")

    def verification_request_answer_generator(self, request_data):
        """Прием зашифрованного сообщения, отправка запроса на проверку для верификации"""
        print("Auth_module: Received crypto message")
        # print(type(request_data['crypto_msg']))
        # print(request_data)
        decrypt_msg = rsa.decrypt(bytes(request_data['crypto_msg']), self.privkey)
        i = 0
        decrypt_mas = []
        while i < len(decrypt_msg):
            decrypt_mas.append(decrypt_msg[i])
            i = i+1
        send_msg = {'nick': request_data['nick'],
                    'pubkey_n': request_data['pubkey_n'],
                    'pubkey_e': request_data['pubkey_e'],
                    'decrypt_msg': decrypt_mas}
        for peer in self.networking.get_peers():
            ver_request = self.send_request(peer, 'auth_request', send_msg)

    def verification_request_answer_received(self, request):
        print("Auth_module: User received crypto message")

    def auth_request_answer_generator(self, request_data):
        """Проверка расшифрованного сообщения"""
        print(bytes(request_data['decrypt_msg']))
        if self.random_msg == bytes(request_data['decrypt_msg']):
            self.users_list.append( {'nick': request_data['nick'],
                                       'pubkey': rsa.PublicKey(request_data['pubkey_n'], request_data['pubkey_e'])} )
            print("User ", request_data['nick'], "is authenticated")
            # print(self.users_list)
            return "Auth_module: Welcome to p2p world!!"
        else:
            print("User ", request_data['nick'], "is not authenticated")
            return "Auth_module: Authentication error!!"

    def auth_request_answer_received(self, request):
        print()
import os
import random
from threading import Timer

from NetworkingModule.NetworkingUsingModule import *


class ConnectionCircleDetector(NetworkingUsingModule):
    """
    У сервера могут быть разные ip, например, localhost и 127.0.0.1.
    Этот модуль проверяет пиров, не являются ли они соединениями "сам к себе".
    """

    def __init__(self, networking, request_processor):
        super().__init__(networking, request_processor, 'connection_circle_detector')
        self.detected_circles = []
        self.detected_not_circled = []
        self.register_callbacks_for_requests()

        self.unique_key = random.random()
        print('Unique instance key:' + repr(self.unique_key))
        self.process()

    def register_callbacks_for_requests(self):
        self.register_request_answer_generator('unique_instance_key', self.get_unique_instance_key)
        self.register_answer_received_callback('unique_instance_key', self.unique_instance_key_received)

    def get_unique_instance_key(self, question_data):
        return self.unique_key

    def unique_instance_key_received(self, request):
        if request.answer_data == self.unique_key:
            print('circle detected')

    def is_peer_checked(self, peer):
        pass

    def is_peer_connection_circle(self, peer):
        pass

    def get_circled_peers(self):
        pass

    def get_not_circled_peers(self):
        pass

    def check_peer(self, peer):
        pass

    def process(self):
        update_timeout = 1

        for peer in self.networking.get_peers():
            if self.get_peer_metadata(peer, 'uid_request') is None:
                request = self.send_request(peer, 'unique_instance_key', 'Hello, boy, give me your server port!')
                self.set_peer_metadata(peer, 'uid_request', request)

        timer = Timer(update_timeout, self.process)
        timer.start()
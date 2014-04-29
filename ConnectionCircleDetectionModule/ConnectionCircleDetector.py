import os
import random
from threading import Timer

from NetworkingModule.NetworkingUsingModule import *
from Interface.AllowingProcessing import *


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
        self.peers_unique_instance_keys = {}

        self.unique_key = random.random()
        print('Unique instance key:' + repr(self.unique_key))
        self.process()

    def register_callbacks_for_requests(self):
        self.register_request_answer_generator('unique_instance_key', self.get_unique_instance_key)
        self.register_answer_received_callback('unique_instance_key', self.unique_instance_key_received)

    def get_unique_instance_key(self, question_data):
        return self.unique_key

    def unique_instance_key_received(self, request):
        self.peers_unique_instance_keys[request.peer] = request.answer_data
        if request.answer_data == self.unique_key:
            if not request.peer in self.detected_circles:
                self.detected_circles.append(request.peer)
        else:
            if not request.peer in self.detected_not_circled:
                self.detected_not_circled.append(request.peer)

    def is_peer_checked(self, peer):
        return peer in self.detected_circles or peer in self.detected_not_circled

    def is_peer_connection_circle(self, peer):
        return peer in self.detected_circles

    def is_peer_non_connection_circled(self, peer):
        return peer in self.detected_not_circled

    def get_circled_peers(self):
        return self.detected_circles

    def get_peer_unique_instance_key(self, peer):
        if peer in self.peers_unique_instance_keys:
            return self.peers_unique_instance_keys[peer]
        else:
            return False

    def get_not_circled_peers(self):
        return self.detected_not_circled

    def check_peer(self, peer):
        if self.get_peer_metadata(peer, 'uid_request') is None:
                request = self.send_request(peer, 'unique_instance_key', 'Hello, boy, give me your server port!')
                self.set_peer_metadata(peer, 'uid_request', request)

    def process(self):
        if not AllowingProcessing().allow_processing:
            print("ConnectionCircleClosed")
            return 0

        update_timeout = 1

        for peer in self.networking.get_peers():
            self.check_peer(peer)

        timer = Timer(update_timeout, self.process)
        timer.start()

    def get_peer_with_unique_key(self, key):
        for peer in self.peers_unique_instance_keys:
            if self.peers_unique_instance_keys[peer] == key:
                return peer
        return None
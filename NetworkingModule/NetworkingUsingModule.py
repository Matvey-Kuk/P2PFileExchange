from time import time

from NetworkingModule.Request import *


class NetworkingUsingModule():

    """Должны унаследовать все классы, использующие Networking"""

    def __init__(self, networking, request_processor ,prefix):
        self.networking = networking
        self.requests_processor = request_processor
        self.prefix = prefix
        self.received_messages = []
        self.requests_in_processing = []
        self.request_re_asking_timeout = 10

    def send_message_to_peer(self, **kwargs):
        if 'peer' in kwargs and 'data' in kwargs:
            self.networking.send_message(Message(kwargs['peer'], prefix=self.prefix, text=kwargs['data']))
        elif 'message' in kwargs:
            self.networking.send_message(kwargs['message'])

    def receive_messages(self):
        return self.networking.get_messages(self.prefix)

    def send_request(self, peer, request_prefix, request_data):
        self.requests_processor.send_request(peer, self.prefix, request_prefix, request_data)

    def register_request_answer_generator(self, request_type, callback):
        self.requests_processor.register_answer_generator_callback(self.prefix, request_type, callback)

    def process(self):
        pass

    def set_peer_metadata(self, peer, data_prefix, data):
        peer.set_metadata(self.prefix, data_prefix, data)

    def get_peer_metadata(self, peer, data_prefix):
        return peer.get_metadata(self.prefix, data_prefix)
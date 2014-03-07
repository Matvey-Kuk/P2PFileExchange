from NetworkingModule.Request import *


class NetworkingUsingModule():

    """Должны унаследовать все классы, использующие Networking"""

    def __init__(self, networking, prefix):
        self.networking = networking
        self.prefix = prefix
        self.received_messages = []
        self.requests_in_processing = []

    def send_message_to_peer(self, peer, data):
        self.networking.send_message(Message(peer, prefix=self.prefix, text=data))

    def receive_messages(self):
        return self.networking.get_messages(self.prefix)

    def generate_new_request_for_peer(self, peer, data):
        request = Reqest()
        self.send_message_to_peer(peer, request.get_message())

    def process_requests(self):
        for request_in_process in self.requests_in_processing:
            pass

    def process(self):
        self.process_requests()

    def set_peer_metadata(self, peer, data_prefix, data):
        peer.set_metadata(self.prefix, data_prefix, data)

    def get_peer_metadata(self, peer, data_prefix):
        peer.get_metadata(self.prefix, data_prefix)
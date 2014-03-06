from NetworkingModule.Request import *


class NetworkingUsingModule():

    """Должны унаследовать все классы, использующие Networking"""

    def __init__(self, networking, prefix):
        self.networking = networking
        self.prefix = prefix
        self.received_messages = []

    def send_message_to_peer(self, peer, data):
        self.networking.send_message(Message(peer, prefix=self.prefix, text=data))

    def receive_messages(self):
        return self.networking.get_messages(self.prefix)

    def send_request_to_peer(self, peer, data):
        self.networking.send_request(Request(peer, data, self.prefix))
from NetworkingModule.Message import *


class NetworkingUsingModule():

    """Должны унаследовать все классы, использующие Networking"""

    def __init__(self, networking, prefix):
        self.networking = networking
        self.prefix = prefix

    def send_message_to_peer(self, peer, data):
        self.networking.send_message(Message(peer, prefix=self.prefix, text=data))

    def receive_messages(self):
        return self.networking.get_messages(self.prefix)

    def set_peer_metadata(self, peer, data_prefix, data):
        peer.set_metadata(self.prefix, data_prefix, data)

    def get_peer_metadata(self, peer, data_prefix):
        peer.get_metadata(self.prefix, data_prefix)
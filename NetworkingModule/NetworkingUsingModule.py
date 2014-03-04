from NetworkingModule.Message import *


class NetworkingUsingModule():

    """Должны унаследовать все классы, использующие Networking"""

    def __init__(self, networking, prefix):
        self.networking = networking
        self.prefix = prefix

    def send_message_to_peer(self, peer, data):
        self.networking.send_message(Message(peer, prefix=self.prefix, text=data))
from Networking.ClientThread import *
from Networking.Message import *


class ClientReceiveThread(ClientThread):

    def __init__(self, peer, socket, received_messages):
        super().__init__(socket)
        self.peer = peer
        self.received_messages = received_messages
        self.received_bytes = bytearray()

    def run(self):
        print("client receive loop started")
        while True:
            received_data = self.socket.recv(1)
            self.received_bytes = b''.join([self.received_bytes, received_data])
            if b'\n' in received_data:
                self.received_messages.put(Message(self.received_bytes, self.peer))
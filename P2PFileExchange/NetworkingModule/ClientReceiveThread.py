from NetworkingModule.ClientThread import *
from NetworkingModule.Message import *


class ClientReceiveThread(ClientThread):

    def __init__(self, peer, socket, received_messages, running_enabled, connection_errors):
        super().__init__(socket)
        self.peer = peer
        self.received_messages = received_messages
        self.received_bytes = bytearray()
        self.running_enabled = running_enabled
        self.connection_errors = connection_errors

    def run(self):
        while self.running_enabled:
            try:
                received_data = self.socket.recv(1)
                self.received_bytes = b''.join([self.received_bytes, received_data])
                if b'\n' in received_data:
                    self.received_messages.put(Message(self.peer, bytes=self.received_bytes))
                    self.received_bytes = bytearray()
            except Exception as exception:
                self.connection_errors.put(exception)
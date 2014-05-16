from NetworkingModule.ClientThread import *


class ClientSendThread(ClientThread):

    def __init__(self, socket, messages_for_sending, enabled, running_enabled, connection_errors):
        super().__init__(socket)
        self.messages_for_sending = messages_for_sending
        self.enabled = enabled
        self.running_enabled = running_enabled
        self.connection_errors = connection_errors

    def run(self):
        while self.running_enabled:
            try:
                self.enabled.wait()
                if self.messages_for_sending.qsize() == 0:
                    self.enabled.clear()
                else:
                    self.socket.sendall(self.messages_for_sending.get().get_bytes() + b'\n')
            except Exception as exception:
                self.connection_errors.put(exception)
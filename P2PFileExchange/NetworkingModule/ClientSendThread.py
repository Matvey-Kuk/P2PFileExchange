from NetworkingModule.ClientThread import *
from Interface.AllowingProcessing import *

from time import sleep


class ClientSendThread(ClientThread):

    def __init__(self, socket, messages_for_sending, enabled, running_enabled, connection_errors):
        super().__init__(socket)
        self.messages_for_sending = messages_for_sending
        self.enabled = enabled
        self.running_enabled = running_enabled
        self.connection_errors = connection_errors

    def run(self):
        while self.running_enabled and AllowingProcessing().allow_processing:
            try:
                if self.messages_for_sending.qsize() != 0:
                    self.socket.sendall(self.messages_for_sending.get().get_bytes() + b'\n')
                else:
                    sleep(0.1)
            except BlockingIOError:
                sleep(0.1)
            except Exception as exception:
                self.connection_errors.put(exception)
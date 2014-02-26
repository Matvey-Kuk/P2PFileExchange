from Networking.ClientThread import *


class ClientSendThread(ClientThread):

    def __init__(self, socket, messages_for_sending, enabled):
        super().__init__(socket)
        self.messages_for_sending = messages_for_sending
        self.enabled = enabled

    def run(self):
        print("client send loop started")
        while True:
            self.enabled.wait()
            print("sending message")
            if self.messages_for_sending.qsize() == 0:
                self.enabled.clear()
            else:
                self.socket.sendall(self.messages_for_sending.get().get_bytes())
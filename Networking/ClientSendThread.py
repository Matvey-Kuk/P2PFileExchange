from Networking.ClientThread import *


class ClientSendThread(ClientThread):

    def __init__(self, socket, send_chunks):
        super().__init__(socket)
        self.send_chunks = send_chunks

    def run(self):
        print("client send loop started")
        while self.send_chunks.qsize() > 0:
            self.socket.sendall(self.send_chunks.get())
import threading
import socket
import inspect

from NetworkingModule.Peer import *


class ServerThread(threading.Thread):

    def __init__(self, host, port, peers):
        threading.Thread.__init__(self)

        self.host = host
        self.port = port
        self.peers = peers

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.tcp_socket.bind((self.host, self.port))

    def run(self):
        while True:
            self.tcp_socket.listen(4)
            (socket, (ip, port)) = self.tcp_socket.accept()
            peer = Peer(ip, port, socket)
            self.peers.append(peer)
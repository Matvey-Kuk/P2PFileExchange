import threading
import socket
import inspect

from Networking.Peer import *


class ServerThread(threading.Thread):

    def __init__(self, host, port):
        threading.Thread.__init__(self)

        self.host = host
        self.port = port

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.tcp_socket.bind((self.host, self.port))

        self.new_connection_callback = None

    def register_new_connection_callback(self, function):
        self.new_connection_callback = function

    def run(self):
        print("Server loop started...")
        while True:
            self.tcp_socket.listen(4)
            (socket, (ip, port)) = self.tcp_socket.accept()
            peer = Peer(ip, port, socket)
            if inspect.isroutine(self.new_connection_callback):
                self.new_connection_callback(peer)
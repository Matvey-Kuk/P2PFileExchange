import threading
import socket


class ServerThread(threading.Thread):

    def __init__(self, host, port):
        threading.Thread.__init__(self)

        self.host = host
        self.port = port

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.tcp_socket.bind((self.host, self.port))

    def register_new_connection_callback(self, function):
        self.new_connection_callback = function

    def run(self):
        print("Server loop started...")
        while True:
            self.tcp_socket.listen(4)
            (clientsock, (ip, port)) = self.tcp_socket.accept()

            print("new connection")
            self.new_connection_callback()
            # #pass clientsock to the ClientThread thread object being created
            # newthread = ClientThread(ip, port, clientsock)
            # newthread.start()
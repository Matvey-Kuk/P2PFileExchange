from Networking.ClientThread import *

class Peer (object):
    """
    Пир- участник сети, о котором знает Networking. Здесь должна храниться вся информация о нем.
    Этот же класс следит за потоком, который обслуживает сокет.
    """

    def __init__(self, ip, port, socket):
        self.ip = ip
        self.port = port
        self.is_alive = False
        self.socket = socket

        self.client_thread = ClientThread(self.ip, self.port, self.socket, self.data_received, self.disconnected)
        self.client_thread.start()

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def is_alive(self):
        return self.is_alive

    def set_is_alive(self, is_alive):
        self.is_alive = is_alive

    def get_socket(self):
        return self.socket

    def data_received(self):
        pass

    def disconnected(self):
        pass
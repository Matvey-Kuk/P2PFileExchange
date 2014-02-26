from threading import Timer
import socket

from Networking.Peer import *
from Networking.ServerThread import *


class Networking(object):
    """ Этот класс обеспечивает все сетевое взаимодействие."""

    def __init__(self, host, port):
        self.peers = []
        self.server_thread = ServerThread(host, port, self.peers)
        self.server_thread.start()
        self.network_using_objects = []

        self.update()
        self.provoke_connection("localhost", 12345)

    def send_data(self, peer, module_name):
        pass

    def get_data(self, module_name):
        return {
            "peer": Peer,
            "data": "some data"
        }

    def get_self_connection_data(self):
        return {
            "ip": "some ip",
            "port": "some port",
            "alive": True
        }

    def register_network_user(self, obj):
        """Здесь нужно решистрировать все объекты, использующие соединение"""
        pass

    def unregister_network_user(self, obj):
        """Здесь нужно разрегистрировать все объекты, которые больше не будут использовать соединение"""
        pass

    def collect_needed_peers(self):
        """Собирает всех пиров, с которыми нужно поддерживать соединение"""
        pass

    def inspect_connections(self):
        """Инспектирует все соединения- доотправляет данные и закрывает ненужные"""
        pass

    def provoke_connection(self, ip, port):
        """
        Провоцирует соединение
        @return: Peer object
        """
        provoked_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        provoked_socket.connect((ip, port))
        new_peer = Peer(ip, port, provoked_socket)
        self.peers.append(new_peer)
        return new_peer

    def process_peers(self):
        for peer in self.peers:
            peer.process_messages()

    def update(self):
        """
        Запускает все переодические операции для соединений
        """
        update_timeout = 1

        self.process_peers()

        timer = Timer(update_timeout, self.update)
        timer.start()
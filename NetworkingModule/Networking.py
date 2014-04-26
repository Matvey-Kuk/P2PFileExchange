from threading import Timer

from NetworkingModule.ServerThread import *
from Interface.AllowingProcessing import *


class Networking(object):
    """ Этот класс обеспечивает все сетевое взаимодействие."""

    def __init__(self, host, port):
        self.server_port = port
        self.peers = []
        self.server_thread = ServerThread(host, port, self.peers)
        self.server_thread.start()
        self.network_using_objects = []

        self.received_messages = []
        self.messages_for_sending = []

        self.update()

    def get_messages(self, prefix, mark_taken_as_read=True):
        """
        Получаем непрочитанные сообщения с данным префиксом.
        Можно пометить как прочтенные после получения, это исключит повторную выдачу.
        По умолчанию - все отмечаются как прочитанные.
        """
        buf_received_messages = []
        result_messages = []
        for message in self.received_messages:
            if message.prefix == prefix:
                result_messages.append(message)
                if not mark_taken_as_read:
                    buf_received_messages.append(message)
            else:
                buf_received_messages.append(message)
        self.received_messages = buf_received_messages
        return result_messages

    def send_message(self, message):
        self.messages_for_sending.append(message)

    def mark_message_as_read(self, message):
        """Помогает отметить конкретное сообщение как прочитанное"""
        self.received_messages.remove(message)

    def get_peers(self):
        return self.peers

    def get_peer(self, ip, port):
        required_peer = None
        for peer in self.peers:
            if peer.ip == ip and peer.port == port:
                required_peer = peer
        return required_peer

    def register_new_peer(self, peer):
        self.peers.append(peer)

    def provoke_connection(self, ip, port):
        """
        Провоцирует соединение
        @return: Peer object
        """
        new_peer = Peer(ip, port)
        new_peer.connect()
        self.register_new_peer(new_peer)
        return new_peer

    def process_peers(self):
        for peer in self.peers:
            buff_messages_for_sending = []

            for message in self.messages_for_sending:
                if message.peer == peer:
                    peer.messages_for_sending.append(message)
                else:
                    buff_messages_for_sending.append(message)
            self.messages_for_sending = buff_messages_for_sending

            peer.process()

            if len(peer.received_messages) > 0:
                self.received_messages = self.received_messages + peer.received_messages
                peer.received_messages = []

    def update(self):
        """
        Запускает все переодические операции для соединений
        """
        if  not AllowingProcessing.allow_processing:
            return 0

        update_timeout = 0.1

        self.process_peers()

        timer = Timer(update_timeout, self.update)
        timer.start()

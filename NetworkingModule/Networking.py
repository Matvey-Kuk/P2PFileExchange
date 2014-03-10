from threading import Timer

from NetworkingModule.ServerThread import *


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
        Можно пометить как прочтенные после получение, это исключит повторную выдачу.
        По умолчанию- все отмечаются как прочитанные.
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

    def register_network_user(self, obj):
        """Здесь нужно решистрировать все объекты, использующие соединение"""
        pass

    def unregister_network_user(self, obj):
        """Здесь нужно разрегистрировать все объекты, которые больше не будут использовать соединение"""
        pass

    def process_peers(self):
        for peer in self.peers:
            buff_messages_for_sending = []

            for message in self.messages_for_sending:
                if message.peer == peer:
                    peer.messages_for_sending.append(message)
                else:
                    buff_messages_for_sending.append(message)
            self.messages_for_sending = buff_messages_for_sending

            peer.process_messages()

            if len(peer.received_messages) > 0:
                self.received_messages = self.received_messages + peer.received_messages
                peer.received_messages = []

    def update(self):
        """
        Запускает все переодические операции для соединений
        """
        update_timeout = 0.1

        self.process_peers()

        timer = Timer(update_timeout, self.update)
        timer.start()

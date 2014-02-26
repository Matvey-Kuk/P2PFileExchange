from queue import *
from threading import Timer

from Networking.ClientReceiveThread import *


class Peer (object):
    """
    Пир- участник сети, о котором знает Networking. Здесь храниться вся информация о нем.
    Этот же класс следит за потоками, которые обслуживают сокет.
    Асинхронно накапливает данные в массивах, откуда их переодически забирает Networking.
    """

    def __init__(self, ip, port, socket):
        self.ip = ip
        self.port = port
        self.is_alive = False
        self.socket = socket

        self.received_messages_queue = Queue()
        self.thread_receive = ClientReceiveThread(self, self.socket, self.received_messages_queue)
        self.thread_receive.start()

        #Информация для Networking копится здесь:
        self.status = {
            "connected": True,
            "messagesAwaitingForSending": 0,
            "receivedMessagesAwaitingForTakingAway": 0
        }
        self.message_for_sending = []
        self.received_messages = []

        self.collect_messages()

    def collect_messages(self):
        """Синхронизирует сообщения между очередями потоков и хранилищами, доступными внешним классам"""
        while self.received_messages_queue.qsize() > 0:
            self.received_messages.append(self.received_messages_queue.get())

        print(self.received_messages)
        timer = Timer(1, self.collect_messages)
        timer.start()
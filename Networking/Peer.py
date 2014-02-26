from queue import *
from threading import Timer

from Networking.ClientReceiveThread import *
from Networking.ClientSendThread import *


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

        self.sending_messages_queue = Queue()
        self.send_enabled = threading.Event()
        self.send_enabled.set()
        self.thread_send = ClientSendThread(self.socket, self.sending_messages_queue, self.send_enabled)
        self.thread_send.start()

        #Информация для Networking копится здесь:
        self.status = {
            "connected": True,
            "messagesAwaitingForSending": 0,
            "receivedMessagesAwaitingForTakingAway": 0
        }
        self.messages_for_sending = []
        self.received_messages = []

        self.process_messages()

    def process_messages(self):
        while self.received_messages_queue.qsize() > 0:
            self.received_messages.append(self.received_messages_queue.get())

        while len(self.messages_for_sending) > 0:
            self.sending_messages_queue.put(self.messages_for_sending.pop(0))

        self.send_enabled.set()

        timer = Timer(1, self.process_messages)
        timer.start()
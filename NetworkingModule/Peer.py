from queue import *
import socket

from NetworkingModule.ClientReceiveThread import *
from NetworkingModule.ClientSendThread import *


class Peer (object):
    """
    Пир- участник сети, о котором знает Networking. Здесь храниться вся информация о нем.
    Этот же класс следит за потоками, которые обслуживают сокет.
    Асинхронно накапливает данные в массивах, откуда их переодически забирает Networking.
    """

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = None
        self.metadata = {}

        self.received_messages_queue = Queue()

        self.sending_messages_queue = Queue()
        self.send_enabled = threading.Event()

        #Информация для Networking копится здесь:
        self.status = {
            #Todo: Обработать отключение пира
            "connected": True,
            "messagesAwaitingForSending": 0,
            "receivedMessagesAwaitingForTakingAway": 0
        }
        self.messages_for_sending = []
        self.received_messages = []

    def connect(self, new_socket=None):
        if new_socket is None:
            provoked_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            provoked_socket.connect((self.ip, self.port))
            self.socket = provoked_socket
        else:
            self.socket = new_socket
        self.start_threads()

    def start_threads(self):
        self.thread_receive = ClientReceiveThread(self, self.socket, self.received_messages_queue)
        self.thread_receive.start()
        self.thread_send = ClientSendThread(self.socket, self.sending_messages_queue, self.send_enabled)
        self.thread_send.start()

    def disconnect(self):
        pass

    def process_messages(self):
        while self.received_messages_queue.qsize() > 0:
            self.received_messages.append(self.received_messages_queue.get())

        while len(self.messages_for_sending) > 0:
            self.sending_messages_queue.put(self.messages_for_sending.pop(0))

        self.send_enabled.set()

    def set_metadata(self, module_prefix, data_prefix, data):
        if not module_prefix in self.metadata:
            self.metadata[module_prefix] = {}
        self.metadata[module_prefix][data_prefix] = data

    def get_metadata(self, module_prefix, data_prefix):
        if module_prefix in self.metadata:
            if data_prefix in self.metadata[module_prefix]:
                return self.metadata[module_prefix][data_prefix]
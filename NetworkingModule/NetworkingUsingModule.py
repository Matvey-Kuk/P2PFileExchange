from time import time

from NetworkingModule.Request import *


class NetworkingUsingModule():

    """Должны унаследовать все классы, использующие Networking"""

    def __init__(self, networking, request_processor ,prefix):
        self.networking = networking
        self.requests_processor = request_processor
        self.prefix = prefix
        self.received_messages = []
        self.requests_in_processing = []
        self.request_re_asking_timeout = 10

    def send_message_to_peer(self, **kwargs):
        """
        Отправить сообщение пиру.
        @param kwargs: Здесь могут быть либо peer и data, либо объект message.
        @return:
        """
        if 'peer' in kwargs and 'data' in kwargs:
            self.networking.send_message(Message(kwargs['peer'], prefix=self.prefix, text=kwargs['data']))
        elif 'message' in kwargs:
            self.networking.send_message(kwargs['message'])

    def receive_messages(self):
        """
        Позволяет получить все новые сообщения для этого модуля.
        @return: Список сообщений.
        """
        return self.networking.get_messages(self.prefix)

    def send_request(self, peer, request_prefix, request_data):
        """
        Отправить запрос.
        @param peer: Пир, который будет отвечать на запрос.
        @param request_prefix: Префикс запроса- уникален для каждого типа запроса.
        @param request_data: Данные, которые уйдут с запросом. Их получит функция, которая будет генерировать
        ответ на стороне пира.
        @return:
        """
        self.requests_processor.send_request(peer, self.prefix, request_prefix, request_data)

    def register_request_answer_generator(self, request_type, callback):
        """
        Здесь нужно зарегистрировать функцию, которая будет отвечать на запросы и генерировать данные для ответа.
        @param request_type: Тип запроса.
        @param callback: Функция.
        """
        self.requests_processor.register_answer_generator_callback(self.prefix, request_type, callback)

    def register_answer_received_callback(self, request_type, callback):
        """
        Здесь нужно зарегистрировать функцию, которая будет вызываться в момент получения ответа на запрос.
        @param request_type: Тип запроса.
        @param callback: Функция.
        """
        self.requests_processor.register_answer_received_callback(self.prefix, request_type, callback)

    def process(self):
        """
        Ничегошеньки.
        """
        pass

    def set_peer_metadata(self, peer, data_prefix, data):
        """
        Пиру можно прилепить какие-то данные, которые будут доступны только из этого модуля по префиксу.
        Перезаписываются данные этой же функцией.
        @param peer: Пир.
        @param data_prefix: Уникальный префикс для этих данных.
        @param data: Сами данные.
        """
        peer.set_metadata(self.prefix, data_prefix, data)

    def get_peer_metadata(self, peer, data_prefix):
        """
        У пира можно забрать данные, выставленные @function set_peer_metadata .
        @param peer: Peer
        @param data_prefix: Префикс данных.
        """
        return peer.get_metadata(self.prefix, data_prefix)
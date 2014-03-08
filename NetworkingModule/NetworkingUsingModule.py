from time import time

from NetworkingModule.Request import *


class NetworkingUsingModule():

    """Должны унаследовать все классы, использующие Networking"""

    def __init__(self, networking, prefix):
        self.networking = networking
        self.prefix = prefix
        self.received_messages = []
        self.requests_in_processing = []
        self.request_re_asking_timeout = 10

    def send_message_to_peer(self, **kwargs):
        if 'peer' in kwargs and 'data' in kwargs:
            self.networking.send_message(Message(kwargs['peer'], prefix=self.prefix, text=kwargs['data']))
        elif 'message' in kwargs:
            self.networking.send_message(kwargs['message'])

    def receive_messages(self):
        return self.networking.get_messages(self.prefix)

    def new_request_for_peer(self, peer, request_class, data_for_question):
        request = request_class(peer=peer, module_prefix=self.prefix, data_for_question=data_for_question)
        self.requests_in_processing.append(request)
        return request

    def process_requests(self):
        received_messages = self.networking.get_messages(Request.messaging_prefix, False)
        for request_in_process in self.requests_in_processing:
            if time() - request_in_process.question_sending_time > self.request_re_asking_timeout:
                self.send_message_to_peer(message=request_in_process.get_question_message())

        for received_message in received_messages:
            print(received_message.get_body())
            for request_in_process in self.requests_in_processing:
                is_answer = request_in_process.check_message_is_answer(received_message)
                if is_answer:
                    self.networking.mark_message_as_read(received_message)

    def process(self):
        self.process_requests()

    def set_peer_metadata(self, peer, data_prefix, data):
        peer.set_metadata(self.prefix, data_prefix, data)

    def get_peer_metadata(self, peer, data_prefix):
        return peer.get_metadata(self.prefix, data_prefix)
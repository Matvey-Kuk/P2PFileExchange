from NetworkingModule.Request import *


class NetworkingUsingModule():

    """Должны унаследовать все классы, использующие Networking"""

    def __init__(self, networking, prefix):
        self.networking = networking
        self.prefix = prefix
        self.received_messages = []
        self.requests_in_processing = []

    def send_message_to_peer(self, **kwargs):
        if 'peer' in kwargs and 'data' in kwargs:
            self.networking.send_message(Message(kwargs['peer'], prefix=self.prefix, text=kwargs['data']))
        elif 'message' in kwargs:
            self.networking.send_message(kwargs['message'])

    def receive_messages(self):
        return self.networking.get_messages(self.prefix)

    def new_request_for_peer(self, peer, data):
        request = Request(peer, data, self.prefix)
        self.requests_in_processing.append(request)
        self.send_message_to_peer(message=request.get_message())

    def process_requests(self):
        received_messages = self.networking.get_messages(Request.messaging_prefix)
        for received_message in received_messages:
            for request_in_process in self.requests_in_processing:
                request_in_process.check_message_is_answer(received_message)
                print(1)

    def process(self):
        self.process_requests()

    def set_peer_metadata(self, peer, data_prefix, data):
        peer.set_metadata(self.prefix, data_prefix, data)

    def get_peer_metadata(self, peer, data_prefix):
        peer.get_metadata(self.prefix, data_prefix)
from threading import Timer

from NetworkingModule.NetworkingUsingModule import *


class P2p(NetworkingUsingModule):
    """Следит за p2p соединением, выпрашивает новых пиров, выбирает более быстрых."""

    peer_request_period = 5

    def __init__(self, networking, requests_processor):
        super().__init__(networking, requests_processor, 'p2p_new_prefix')
        self.register_request_answer_generator('server_port', self.server_port_request_answer)
        self.register_answer_received_callback('server_port', self.server_port_answer_received)
        self.process()

    def server_port_request_answer(self, question_data):
        print('generating answer')
        return self.networking.server_port

    def server_port_answer_received(self, request):
        print('answer received')
        self.set_peer_metadata(request.peer, 'server_port', request.answer_data)

    def process(self):
        super().process()
        update_timeout = 1

        self.ask_server_port()
        self.ask_new_peers()

        timer = Timer(update_timeout, self.process)
        timer.start()

    def ask_server_port(self):
        for peer in self.networking.get_peers():
            if self.get_peer_metadata(peer, 'server_port_request') is None:
                request = self.send_request(peer, 'server_port', 'Hello, boy, give me your server port!')
                request.set_periodically(5)
                self.set_peer_metadata(peer, 'server_port_request', request)

    def ask_new_peers(self):
        pass
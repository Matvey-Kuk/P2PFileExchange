from threading import Timer

from NetworkingModule.NetworkingUsingModule import *


class P2p(NetworkingUsingModule):
    """Следит за p2p соединением, выпрашивает новых пиров, выбирает более быстрых."""

    peer_request_period = 5

    def __init__(self, networking, requests_processor):
        super().__init__(networking, requests_processor, 'p2p_new_prefix')
        self.register_callbacks_for_requests()
        self.process()

    def register_callbacks_for_requests(self):
        self.register_request_answer_generator('server_port', self.server_port_request_answer)
        self.register_answer_received_callback('server_port', self.server_port_answer_received)

        self.register_request_answer_generator('peers_request', self.peer_request_answer)
        self.register_answer_received_callback('peers_request', self.peer_request_answer_received)

    def peer_request_answer(self, question_data):
        peer_list = []
        for peer in self.networking.get_peers():
            if not self.get_peer_metadata(peer, 'server_port') is None:
                peer_list.append({
                    'ip': peer.ip,
                    'server_port': self.get_peer_metadata(peer, 'server_port')
                })
        return peer_list

    def peer_request_answer_received(self, request):
        print('received peers: ' + repr(request.answer_data))
        all_server_ports_are_known = True
        peer_list = []
        for peer in self.networking.get_peers():
            if self.get_peer_metadata(peer, 'server_port') is None:
                all_server_ports_are_known = False
            else:
                peer_list.append({
                    'ip': peer.ip,
                    'server_port': self.get_peer_metadata(peer, 'server_port')
                })

        if all_server_ports_are_known:
            new_peers = request.answer_data
            for new_peer in new_peers:
                if not new_peer in peer_list:
                    print('provoked with ' + new_peer['ip'] + ":" + str(new_peer['server_port']))
                    self.networking.provoke_connection(new_peer['ip'], new_peer['server_port'])

    def server_port_request_answer(self, question_data):
        return self.networking.server_port

    def server_port_answer_received(self, request):
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
                self.set_peer_metadata(peer, 'server_port_request', request)

    def ask_new_peers(self):
        for peer in self.networking.get_peers():
            if self.get_peer_metadata(peer, 'peers_request') is None:
                request = self.send_request(peer, 'peers_request', None)
                request.set_periodically(10)
                self.set_peer_metadata(peer, 'peers_request', request)
from threading import Timer

from NetworkingModule.NetworkingUsingModule import *
from NetworkingModule.Peer import *
from Interface.AllowingProcessing import *
from Interface.Interface import *


class P2p(NetworkingUsingModule):
    """Следит за p2p соединением, выпрашивает новых пиров, выбирает более быстрых."""

    peer_request_period = 5

    def __init__(self, networking, requests_processor, circle_detector):
        super().__init__(networking, requests_processor, 'p2p_new_prefix')
        self.circle_detector = circle_detector
        self.register_callbacks_for_requests()
        self.register_interface_callbacks()
        self.process()

    def register_callbacks_for_requests(self):
        self.register_request_answer_generator('server_port', self.server_port_request_answer)
        self.register_answer_received_callback('server_port', self.server_port_answer_received)

        self.register_request_answer_generator('peers_request', self.peer_request_answer)
        self.register_answer_received_callback('peers_request', self.peer_request_answer_received)

    def peer_request_answer(self, question_data, peer):
        peer_list = []
        peer_added_list = []
        for peer in self.networking.get_peers():
            if self.circle_detector.is_peer_non_connection_circled:
                if not self.get_peer_metadata(peer, 'server_port') is None:
                    if not peer in peer_added_list:
                        peer_list.append({
                            'ip': peer.ip,
                            'server_port': self.get_peer_metadata(peer, 'server_port'),
                            'unique_key': self.circle_detector.get_peer_unique_instance_key(peer)
                        })
                        peer_added_list.append(peer)
        return peer_list

    def peer_request_answer_received(self, request):
        all_server_ports_are_known = True
        all_unique_keys_checked = True
        for peer in self.networking.get_peers():
            if not self.circle_detector.is_peer_checked(peer):
                all_unique_keys_checked = False
            if self.get_peer_metadata(peer, 'server_port') is None:
                all_server_ports_are_known = False

        if all_server_ports_are_known and all_unique_keys_checked:
            new_peers = request.answer_data
            for new_peer in new_peers:
                if self.circle_detector.get_peer_with_unique_key(new_peer['unique_key']) is None and self.circle_detector.unique_key != new_peer['unique_key']:
                    if self.networking.get_peer(new_peer['ip'], new_peer['server_port']) is None:
                        self.networking.provoke_connection(new_peer['ip'], new_peer['server_port'])

    def server_port_request_answer(self, question_data, peer):
        return self.networking.server_port

    def server_port_answer_received(self, request):
        self.set_peer_metadata(request.peer, 'server_port', request.answer_data)

    def process(self):
        if not AllowingProcessing().allow_processing:
            print("P2PClosed")
            return 0

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

    def send_data_to_interface(self):
        s = "Number of peers: %d" % len(self.networking.peers)
        return s

    def process_interface_command(self, command):
        if command == 'show peers':
            return repr(self.networking.get_peers())
        return 'Undefined command'

    def register_interface_callbacks(self):
        Interface.register_output_callback('p2p', self.send_data_to_interface)
        Interface.register_command_processor_callback('p2p', self.process_interface_command)
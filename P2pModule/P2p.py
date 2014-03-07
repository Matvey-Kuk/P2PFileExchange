from threading import Timer
from time import time

from NetworkingModule.NetworkingUsingModule import *
from P2pModule.DormantPeer import *


class P2p(NetworkingUsingModule):
    """Следит за p2p соединением, выпрашивает новых пиров, выбирает более быстрых."""

    command_give_me_peers = 'give_me_peers'
    command_give_me_your_server_port = 'give_me_tour_server_port'
    command_timeout = 1

    peer_request_period = 5

    def __init__(self, networking):
        super().__init__(networking, 'p2p_new_prefix')
        self.dormant_peers = []
        self.networking = networking
        self.process()

    def process(self):
        super().process()
        update_timeout = 1

        self.ask_new_peers()
        # self.check_availability_of_server_ports()
        # self.initialise_connections()
        #
        # received_messages = self.receive_messages()
        # for message in received_messages:
        #     self.request_processor(message)

        timer = Timer(update_timeout, self.process)
        timer.start()

    def initialise_connections(self):
        print("dormant:")
        for dormant_peer in self.dormant_peers:
            print(dormant_peer.ip + ":" + str(dormant_peer.server_port))
        for dormant_peer in self.dormant_peers:
            if dormant_peer.connection_provoked_to_peer is None:
                provoked_with_peer = self.networking.provoke_connection(dormant_peer.ip, dormant_peer.server_port)
                dormant_peer.connection_provoked(provoked_with_peer)
                print("provoked from dormant")

    def ask_server_port(self, peer):
        print("requested server port")
        self.set_peer_metadata(peer, 'server_port_requested_time', time())
        self.send_message_to_peer(peer, self.command_give_me_your_server_port)

    def check_availability_of_server_ports(self):
        for peer in self.networking.get_peers():
            if self.get_peer_metadata(peer, 'server_port') is None:
                if self.get_peer_metadata(peer, 'server_port_requested_time') is None:
                    self.ask_server_port(peer)
                elif time() - self.get_peer_metadata(peer, 'server_port_requested_time') > self.command_timeout:
                    self.ask_server_port(peer)

    def ask_new_peers(self):
        for peer in self.networking.get_peers():
            if self.get_peer_metadata(peer, 'server_port_request') is None:
                request = self.new_request_for_peer(peer, "ping")

    def tell_about_known_peers(self, peer):
        peers_list_for_sending = []
        for peer in self.networking.get_peers():
            if not self.get_peer_metadata(peer, 'server_port') is None:
                peers_list_for_sending.append({'ip': peer.ip, 'port': self.get_peer_metadata(peer, 'server_port')})
        self.send_message_to_peer(peer, {"command": "my_peers", "peers": peers_list_for_sending})

    def tell_about_my_server_port(self, peer):
        self.send_message_to_peer(peer, {"command": "my_server_port","port":self.networking.server_port})

    def request_processor(self, received_message):
        if received_message.text == self.command_give_me_peers:
            self.tell_about_known_peers(received_message.peer)
        elif received_message.text == self.command_give_me_your_server_port:
            self.tell_about_my_server_port(received_message.peer)
        elif isinstance(received_message.text, dict):
            if received_message.text['command'] == 'my_peers':
                self.received_peers(received_message.peer, received_message.text["peers"])
            if received_message.text['command'] == 'my_server_port':
                self.received_server_port(received_message.peer, received_message.text["port"])

    def received_server_port(self, from_peer, server_port):
        self.set_peer_metadata(from_peer, 'server_port', server_port)

    def received_peers(self, from_peer, peers):
        print('Received peers:' + repr(peers))
        for peer in peers:
            all_peers_sent_server_ports = True
            peer_is_known_as_local_peer = None
            peer_is_known_as_dormant = None
            for dormant_peer in self.dormant_peers:
                if dormant_peer.ip == peer['ip'] and dormant_peer.server_port == peer['port']:
                    print('known')
                    peer_is_known_as_dormant = dormant_peer

            for local_peer in self.networking.get_peers():
                if self.get_peer_metadata(local_peer, 'server_port') is None:
                    all_peers_sent_server_ports = False
                else:
                    if peer['port'] == self.get_peer_metadata(local_peer, 'server_port') and peer['ip'] == local_peer.ip:
                        peer_is_known_as_local_peer = local_peer

            if all_peers_sent_server_ports:
                if not peer_is_known_as_dormant is None:
                    peer_is_known_as_dormant.detected(from_peer)
                else:
                    if peer_is_known_as_local_peer is None:
                        self.dormant_peers.append(DormantPeer(from_peer, peer['ip'], peer['port']))
import argparse

from NetworkingModule.Networking import *
from P2pModule.P2p import *
from RequestsModule.RequestsProcessor import *
from ConnectionCircleDetectionModule.ConnectionCircleDetector import *


class Main(object):
    """Это основной класс, через который запускается приложение."""

    def __init__(self):
        self.command_line_arguments = self.parse_arguments()
        self.networking = self.start_networking()
        self.requests_processor = RequestsProcessor(self.networking)

        self.connection_circle_detector = ConnectionCircleDetector(self.networking, self.requests_processor)
        self.p2p = P2p(self.networking, self.requests_processor)

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Hello, p2p world.')
        parser.add_argument('-port', '-p', dest='port', help='Server port')
        parser.add_argument('-host', dest='bind_host', help='Host for server binding')
        parser.add_argument('-peer', dest='first_peer', help='ip:port of first peer needed for connection')
        command_line_args = parser.parse_args()
        return command_line_args

    def start_networking(self):
        port = 1234
        if not self.command_line_arguments.port is None:
            port = int(self.command_line_arguments.port)

        bind_host = "0.0.0.0"
        if not self.command_line_arguments.bind_host is None:
            bind_host = int(self.command_line_arguments.bind_host)

        print("Server started, connection point:\"" + bind_host + ":" + str(port) + "\"")

        networking = Networking(bind_host, port)

        if not self.command_line_arguments.first_peer is None:
            ip_port = self.command_line_arguments.first_peer.split(':')
            peer_ip = ip_port[0]
            peer_port = ip_port[1]
            networking.provoke_connection(peer_ip, int(peer_port))

        return networking

main = Main()
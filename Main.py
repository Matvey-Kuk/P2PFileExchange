import argparse

from Networking import Networking


class Main(object):
    """Это основной класс, через который запускается приложение."""

    def __init__(self):
        parser = argparse.ArgumentParser(description='Hello, p2p world.')
        parser.add_argument('-port', '-p', dest='port', help='Server port')
        parser.add_argument('-host', '-h', dest='bind_host', help='Host for server binding')
        command_line_args = parser.parse_args()

        port = 1234
        if not command_line_args.port is None:
            port = int(command_line_args.port)

        bind_host = "0.0.0.0"
        if not command_line_args.bind_host is None:
            bind_host = int(command_line_args.bind_host)

        networking = Networking.Networking(bind_host, port)

main = Main()
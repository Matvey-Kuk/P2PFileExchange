from threading import Timer

from NetworkingModule.NetworkingInterface import *
from NetworkingModule.Message import *


class P2p(NetworkingInterface):
    """Следит за p2p соединением, выпрашивает новых пиров, выбирает более быстрых."""

    def __init__(self, networking):
        super().__init__()
        self.networking = networking
        self.process()

    def get_needed_peers(self):
        return []

    def process(self):
        update_timeout = 5

        print("P2p processing...")

        for peer in self.networking.get_peers():
            self.networking.send_message(Message(peer, prefix='p2p', text='Hello, p2p!'))

        received_messages = self.networking.get_messages('p2p')
        if len(received_messages) > 0:
            for message in received_messages:
                print("Received:" + message.text)

        timer = Timer(update_timeout, self.process)
        timer.start()
from Networking import NetworkingUser
from Networking import Peer

class P2p(NetworkingUser):
    """Следит за p2p соединением, выпрашивает новых пиров, выбирает более быстрых."""

    def __init__(self):
        pass

    def get_needed_peers(self):
        return [Peer]
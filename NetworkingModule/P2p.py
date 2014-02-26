from NetworkingModule import NetworkingInterface


class P2p(NetworkingInterface.NetworkingInterface):
    """Следит за p2p соединением, выпрашивает новых пиров, выбирает более быстрых."""

    def __init__(self):
        super().__init__()

    def get_needed_peers(self):
        return []
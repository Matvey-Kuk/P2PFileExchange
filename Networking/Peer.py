

class Peer (object):
    """Пир- участник сети, о котором знает Networking. Здесь должна храниться вся информация о нем."""

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.is_alive = False

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def is_alive(self):
        return self.is_alive

    def set_is_alive(self, is_alive):
        self.is_alive = is_alive
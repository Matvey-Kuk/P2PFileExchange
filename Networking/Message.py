class Message(object):
    """Сообщение, передаваемое от пира, или пиру"""

    def __init__(self, body, peer):
        self.body = body
        self.peer = peer

        self._produced = False

    def mark_processed(self):
        self._produced = True

    def is_produced(self):
        return self._produced

    def get_bytes(self):
        return bytearray(self.body, "ascii")
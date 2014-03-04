import json


class Message(object):
    """Сообщение, передаваемое от пира, или пиру"""

    def __init__(self, peer, **kwargs):
        """
        @param peer: Указатель на пира, с которым связано это сообщение
        @param kwargs: либо 'bytes', либо 'prefix' и 'text' - используютя для создания объекта
        """
        self.peer = peer
        self.prefix = ""
        self.data = ""

        if 'bytes' in kwargs:
            body = kwargs['bytes'].decode("ascii")
            body = json.JSONDecoder().decode(body)
            self.prefix = body['prefix']
            self.data = body['text']
        elif 'prefix' in kwargs and 'text' in kwargs:
            self.prefix = kwargs['prefix']
            self.data = kwargs['text']
        else:
            raise NotImplementedError("Не указаны необходимые параметры для создания объекта")

    def get_body(self):
        return json.JSONEncoder().encode({
            'prefix': self.prefix,
            'text': self.data
        })

    def get_bytes(self):
        return bytearray(self.get_body(), "ascii")
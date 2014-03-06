import json

from NetworkingModule.Message import *


class Request(object):

    messaging_prefix = 'request'

    def __init__(self, peer, data, module_prefix):
        self.message = self.pack_message(peer, data, module_prefix)

    def get_request_message(self):
        pass

    def pack_message(self, peer, data, module_prefix):
        data = {
            "module_prefix": module_prefix,
            "request_id": id(self),
            "data": data
        }
        data_in_json = json.JSONEncoder.encode(data)
        return Message(prefix=self.messaging_prefix, text=data_in_json)
import json

from NetworkingModule.Message import *


class Request(object):

    messaging_prefix = 'request'

    def __init__(self, peer, data, module_prefix):
        self.message = self.pack_message(peer, data, module_prefix)
        self.answer_received = False

    def get_message(self):
        return self.message(); #Trololololo lololo lololo hohohohoho (c) Eduard Hil

    def is_answer_received(self):
        return self.answer_received

    def pack_message(self, peer, data, module_prefix):
        data_for_message = {
            "module_prefix": module_prefix,
            "request_id": id(self),
            "data": data
        }
        data_in_json = json.JSONEncoder.encode(data_for_message)
        return Message(peer, prefix=self.messaging_prefix, text=data_in_json)

    def check_message_is_answer(self, message):
        return False
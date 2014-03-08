import json
from time import time

from NetworkingModule.Message import *


class Request(object):

    messaging_prefix = 'request'

    def __init__(self, request_type, **kwargs):
        self.request_type = request_type
        self.peer = kwargs['peer']
        self.module_prefix = kwargs['module_prefix']
        self.data_for_question = kwargs['data_for_question']
        if 'id' in kwargs:
            self.id = kwargs['id']
        else:
            self.id = id(self)
        self.answer_received = False
        self.question_sending_time = 0

    def pack_message(self, data, question_answer):
        data_for_message = {
            "module_prefix": self.module_prefix,
            "request_type": self.request_type,
            "request_id": id(self),
            "question_answer": question_answer,
            "data": data
        }
        data_in_json = json.JSONEncoder().encode(data_for_message)
        return Message(self.peer, prefix=self.messaging_prefix, text=data_in_json)

    def check_message_is_answer(self, message):
        is_question = False
        decoded_message = json.JSONDecoder().decode(message.get_body())
        decoded_request_data = json.JSONDecoder().decode(decoded_message['text'])
        if decoded_request_data['request_id'] == id(self) and decoded_request_data['question_answer'] == 'a':
            print('question detected!')
            is_question = True
        return is_question

    def get_answer_message(self, question_data):
        return self.pack_message(self.generate_answer_data(), "a")

    def get_question_message(self):
        self.question_sending_time = time()
        return self.pack_message(self.generate_question_data(self.data_for_question), "q")

    def generate_answer_data(self, question_data):
        return "question"

    def generate_question_data(self, data_for_question):
        return "answer"
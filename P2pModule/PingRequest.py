from NetworkingModule.Request import *


class PingRequest(Request):

    def __init__(self, **kwargs):
        super().__init__("pinger", **kwargs)

    def generate_answer_data(self, question_data):
        return "pong"

    def generate_question_data(self, data_for_question):
        return "ping"
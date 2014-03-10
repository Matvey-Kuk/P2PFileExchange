from threading import Timer
from time import time

from RequestsModule.Request import *


class RequestsProcessor(object):

    prefix = 'requests_processor'

    def __init__(self, networking):

        self.networking = networking
        self.answer_generating_callbacks = []
        self.non_processed_requests = []

        self.process_requests()

    def send_request(self, peer, module_prefix, request_prefix, question_data):
        request = Request(peer, self.prefix, module_prefix, request_prefix, question_data)
        self.non_processed_requests.append(request)
        return request

    def register_answer_generator_callback(self, module_prefix, request_type, callback):
        pass

    def register_answer_received_callback(self, module_prefix, request_type, callback):
        pass

    def process_requests(self):
        update_timeout = 0.1

        for request in self.non_processed_requests:
            if request.question_sending_needed():
                self.networking.send_message(request.generate_question_message())
                request.question_sent()

        print(self.networking.get_messages(self.prefix))

        timer = Timer(update_timeout, self.process_requests)
        timer.start()
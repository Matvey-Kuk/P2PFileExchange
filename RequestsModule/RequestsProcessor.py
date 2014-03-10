

class RequestsProcessor(object):

    def __init__(self, networking):
        self.networking = networking
        self.requests_types = []

    def register_new_request_type(self, type):
        self.requests_types.append(type)

    def register_answer_generator_callback(self, module_prefix):
        pass
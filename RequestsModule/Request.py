from NetworkingModule.Message import *
from RequestsModule.RequestsProcessor import *


class Request(object):
    """
    Хранит информацию о ходе выполнения запроса.
    """

    question_sending_timeout = 10

    def __init__(self, peer, request_processor_prefix, module_prefix, request_prefix, question_data):

        self.answer_received = False
        self.question_has_been_sent = False

        self.question_sending_time = None
        self.answer_receiving_time = None

        self.peer = peer
        self.module_prefix = module_prefix
        self.request_prefix = request_prefix
        self.request_processor_prefix = request_processor_prefix

        self.question_data = question_data
        self.answer_data = None

    def generate_question_message(self):
        question_data = {
            'request_question_answer': 'question',
            'request_id': id(self),
            'module_prefix': self.module_prefix,
            'request_prefix': self.request_prefix,
            'request_data': self.question_data
        }
        return Message(self.peer, prefix=self.request_processor_prefix, text=question_data)

    def check_message_is_answer(self, message):
        message_decoded = json.JSONDecoder().decode(message.get_body())
        print(message_decoded)
        if message_decoded['text']['request_id'] == id(self) and message_decoded['text']['request_question_answer'] == 'answer' and message.peer == self.peer:
            self.answer_received = True
            self.answer_receiving_time = time()
            self.answer_data = message_decoded['text']['request_data']
            print('answer detected')
            return True
        else:
            return False

    def question_sent(self):
        self.question_has_been_sent = True
        self.question_sending_time = time()

    def question_sending_needed(self):
        return (not self.question_has_been_sent or time() - self.question_sending_time > self.question_sending_timeout) and not self.answer_received
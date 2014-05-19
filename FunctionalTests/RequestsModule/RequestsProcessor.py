from threading import Timer
from time import time
import json

from RequestsModule.Request import *
from Interface.AllowingProcessing import *


class RequestsProcessor(object):

    """
    Процессор запросов, следит за ними и работает циклично в фоне.
    """

    prefix = 'requests_processor'

    def __init__(self, networking):

        self.networking = networking
        self.answer_generating_callbacks = {}
        self.answer_received_callbacks = {}
        self.non_processed_requests = []

        self.process_requests()

    def send_request(self, peer, module_prefix, request_prefix, question_data):
        """
        Отправляем запрос.
        @param peer: Пир.
        @param module_prefix: Префикс модуля.
        @param request_prefix: Тип(префикс) запроса.
        @param question_data: Данные, которые можно отправить с запросом.
        @return:
        """
        request = Request(peer, self.prefix, module_prefix, request_prefix, question_data)
        self.non_processed_requests.append(request)
        return request

    def register_answer_generator_callback(self, module_prefix, request_prefix, callback):
        """
        Здесь нужно зарегистрировать функцию, которая будет генерировать ответные данные на конкретный тип запросов.
        @param module_prefix: Префикс модуля.
        @param request_prefix: Префикс запроса.
        @param callback: Функция, которая выдаст ответ на данный запрос.
        @return:
        """
        if not module_prefix in self.answer_generating_callbacks:
            self.answer_generating_callbacks[module_prefix] = {}
        self.answer_generating_callbacks[module_prefix][request_prefix] = callback

    def register_answer_received_callback(self, module_prefix, request_prefix, callback):
        """
        Здесь нужно зарегистрировать функцию, которая будет вызываться, когда запрос выполнен.
        @param module_prefix: Префикс модуля.
        @param request_prefix: Префикс запроса.
        @param callback: Функция, которая обработает успешное срабатывание запроса.
        @return:
        """
        if not module_prefix in self.answer_received_callbacks:
            self.answer_received_callbacks[module_prefix] = {}
        self.answer_received_callbacks[module_prefix][request_prefix] = callback

    def process_requests(self):
        """
        Системная функция, перемалывает запросы и вызывает коллбэки.
        """

        update_timeout = 2

        new_non_processed_requests = []
        for request in self.non_processed_requests:
            if not request.answer_received or request.is_periodically():
                new_non_processed_requests.append(request)
        self.non_processed_requests = new_non_processed_requests

        for request in self.non_processed_requests:
            if request.question_sending_needed():
                self.networking.send_message(request.generate_question_message())
                request.question_sent()

        messages = self.networking.get_messages(self.prefix)
        for message in messages:
            message_body_json = message.get_body()
            message_body = json.JSONDecoder().decode(message_body_json)
            if message_body['text']['request_question_answer'] == 'question':
                self.process_question(message.peer, message_body)
            for request in self.non_processed_requests:
                if message_body['text']['request_question_answer'] == 'answer':
                    is_answer = request.check_message_is_answer(message)
                    if is_answer:
                        self.answer_received_callbacks[message_body['text']['module_prefix']][message_body['text']['request_prefix']](request)
        timer = Timer(update_timeout, self.process_requests)
        timer.start()

    def process_question(self, peer, message_body):
        """
        Генерирует ответы на чужие запросы через вызов коллбэков.
        """
        module_prefix = message_body['text']['module_prefix']
        request_prefix = message_body['text']['request_prefix']
        request_data = message_body['text']['request_data']
        answer = None
        if module_prefix in self.answer_generating_callbacks:
            if request_prefix in self.answer_generating_callbacks[module_prefix]:
                callback = self.answer_generating_callbacks[module_prefix][request_prefix]
                answer = callback(request_data, peer)
        answer_message = {
            'request_question_answer': 'answer',
            'request_id': message_body['text']['request_id'],
            'module_prefix': module_prefix,
            'request_prefix': request_prefix,
            'request_data': answer
        }
        self.networking.send_message(Message(peer, prefix=self.prefix, text=answer_message))
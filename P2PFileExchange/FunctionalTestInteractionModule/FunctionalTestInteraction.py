from Interface.Interface import *
from NetworkingModule.Networking import *
from NetworkingModule.Message import *
from NetworkingModule.NetworkingUsingModule import *
from RequestsModule.RequestsProcessor import *


class FunctionalTestInteraction(NetworkingUsingModule):

    def __init__(self, port):
        networking = Networking('127.0.0.1', int(port))
        super().__init__(networking, RequestsProcessor(networking), 'functional_testing')

        self.register_request_answer_generator('command', self.received_command)

        print('Started interaction with functional tests on port:' + str(port))

    def received_command(self, request_data, peer):
        print('Received command: ' + request_data)
        return 'boooooo'
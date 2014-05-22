from time import sleep
import argparse
import os

from .Instance import *
from NetworkingModule.Networking import *
from NetworkingModule.NetworkingUsingModule import *
from RequestsModule.RequestsProcessor import *


class FunctionalTestEngine(NetworkingUsingModule):

    def __init__(self):
        AllowingProcessing().allow_processing = True

        networking = Networking('127.0.0.1', 0)
        super().__init__(networking, RequestsProcessor(networking), 'functional_testing')
        self.register_answer_received_callback('command', self.answer_received)

        self.parser = argparse.ArgumentParser(description='Hello, p2p world testing.')
        self.parser.add_argument('-path', '-p', dest='path', help='Test program path')
        self.__server_port_increment = 1111
        self.__last_started_server_port = None
        self.__functional_port_increment = 2111
        self.__instances = []

    @staticmethod
    def is_port_opened(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = not sock.connect_ex(('127.0.0.1', port)) == 0
        sock.close()
        return result

    @staticmethod
    def find_free_port(start_port):
        result_port = start_port
        while not FunctionalTestEngine.is_port_opened(result_port):
            result_port += 1
        return result_port

    def answer_received(self, request):
        pass

    def make_instance(self):
        self.__server_port_increment = FunctionalTestEngine.find_free_port(self.__server_port_increment)
        self.__functional_port_increment = FunctionalTestEngine.find_free_port(self.__functional_port_increment)
        instance = Instance(
            os.path.abspath(__file__)[0:os.path.abspath(__file__).rfind('/')] + '/../../../Main.py',
            self.__server_port_increment,
            self.__functional_port_increment,
            self.__last_started_server_port
        )
        self.__last_started_server_port = self.__server_port_increment
        self.__instances.append(instance)
        sleep(1)
        self.networking.provoke_connection('127.0.0.1', self.__functional_port_increment)
        self.__server_port_increment += 1
        self.__functional_port_increment += 1
        return instance

    def send_command(self, instance, command):
        peer_for_instance = None
        for peer in self.networking.get_peers():
            if peer.port == instance.get_functional_testing_port():
                peer_for_instance = peer
        request = self.send_request(peer_for_instance, 'command', command)
        while request.answer_data is None:
            sleep(0.01)
        return request.answer_data

    def kill_instances(self):
        AllowingProcessing.allow_processing = False
        for instance in self.__instances:
            instance.kill()
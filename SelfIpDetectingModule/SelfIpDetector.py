from threading import Timer
from Interface.AllowingProcessing import *
from NetworkingModule.NetworkingUsingModule import *


class SelfIpDetector(NetworkingUsingModule):
    """
    Модуль выясняет, под каким ip инстанс известен другим пирам.
    """

    def __init__(self, networking, requests_processor):
        super().__init__(networking, requests_processor, 'self_ip_detector')

        self.__ips = []

        self.register_request_answer_generator('self_ip_request', self.self_ip_request_answer_generator)
        self.register_answer_received_callback('self_ip_request', self.self_ip_request_answer_received)

        self.__process()

    def self_ip_request_answer_generator(self, question_data, peer):
        print(question_data)
        print(peer)
        return 'ah'

    def self_ip_request_answer_received(self, request):
        print(request)

    def __process(self):
        if not AllowingProcessing().allow_processing:
            return 0

        for peer in self.networking.get_peers():
            if self.get_peer_metadata(peer, 'ip_request') is None:
                request = self.send_request(peer, 'self_ip_request', 'Hello, give me my ip!')
                self.set_peer_metadata(peer, 'ip_request', request)
            else:
                print(self.get_peer_metadata(peer, 'ip_request'))

        update_timeout = 1

        timer = Timer(update_timeout, self.__process)
        timer.start()
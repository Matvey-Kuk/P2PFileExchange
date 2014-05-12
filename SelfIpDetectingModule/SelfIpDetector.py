from NetworkingModule.NetworkingUsingModule import *


class SelfIpDetector(NetworkingUsingModule):
    """
    Модуль выясняет, под каким ip инстанс известен другим пирам.
    """

    def __init__(self, networking, requests_processor):
        super().__init__(networking, requests_processor, 'self_ip_detector')
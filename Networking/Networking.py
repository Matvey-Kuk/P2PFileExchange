from Networking import Peer


class Networking(object):
    """ Этот класс обеспечивает все сетевое взаимодействие."""

    network_using_objects = []

    def __init__(self):
        pass

    def send_data(self, peer, module_name):
        pass

    def get_data(self, module_name):
        return {
            "peer": Peer,
            "data": "some data"
        }

    def get_self_connection_data(self):
        return {
            "ip": "some ip",
            "port": "some port",
            "alive": True
        }

    def register_network_user(self, obj):
        """Здесь нужно решистрировать все объекты, использующие соединение"""
        pass

    def unregister_network_user(self, obj):
        """Здесь нужно разрегистрировать все объекты, которые больше не будут использовать соединение"""
        pass

    def collect_needed_peers(self):
        """Собирает всех пиров, с которыми нужно поддерживать соединение"""
        pass

    def inspect_connections(self):
        """Инспектирует все соединения- доотправляет данные и закрывает ненужные"""
        pass
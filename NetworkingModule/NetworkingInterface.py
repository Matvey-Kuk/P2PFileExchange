

class NetworkingInterface():

    """Должны унаследовать все классы, использующие Networking"""

    def __init__(self):
        pass

    def get_needed_peers(self):
        """Через этот метод необходимо сообщать список всех пиров, с которыми необходимо соединение, либо []"""
        raise NotImplementedError( "Should have implemented this" )
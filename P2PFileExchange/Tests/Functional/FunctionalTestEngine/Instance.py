import subprocess
import sys


class Instance(object):
    """
    Этот класс описывает объект, который представляет конкретный запущенный экземпляр.
    """

    def __init__(self, run_command, server_port, functional_testing_port, another_peer_server_port=None):
        arguments = [
            'python3',
            run_command,
            '-port',
            str(server_port),
            '-P2PModule',
            '-UsersDatabaseModule',
            '-functionalTestInteractionPort',
            str(functional_testing_port)
        ]
        if not another_peer_server_port is None:
            arguments += [
                '-peer',
                '127.0.0.1:' + str(another_peer_server_port)
            ]
        self.process = subprocess.Popen(
            arguments,
            stdout=subprocess.PIPE,
            shell=False,
        )
        self.__server_port = server_port
        self.__functional_testing_port = functional_testing_port
        self.__another_peer_server_port = another_peer_server_port

    def get_functional_testing_port(self):
        return self.__functional_testing_port

    def get_server_port(self):
        return self.__server_port

    def kill(self):
        self.process.kill()
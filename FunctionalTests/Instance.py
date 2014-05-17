import subprocess
import sys


class Instance(object):
    """
    Этот класс описывает объект, который представляет конкретный запущенный экземпляр.
    """

    def __init__(self, run_command, server_port, functional_testing_port):
        print('started')
        self.process = subprocess.Popen(
            [
                'python3',
                run_command,
                '-port',
                str(server_port),
                '-P2PModule',
                '-UsersDatabaseModule',
                '-functionalTestInteractionPort',
                str(functional_testing_port)
            ],
            shell=False,
        )

    def send_command(self, command):
        pass

    def kill(self):
        self.process.kill()
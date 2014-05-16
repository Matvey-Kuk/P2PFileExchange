import subprocess
import sys


class Instance(object):
    """
    Этот класс описывает объект, который представляет конкретный запущенный экземпляр.
    """

    def __init__(self, run_command, arguments):
        self.process = subprocess.Popen(
            ['python3', run_command, arguments],
            shell=False
        )

    def send_command(self, command):
        pass

    def kill(self):
        self.process.kill()
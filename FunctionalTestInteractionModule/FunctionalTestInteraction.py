from Interface.Interface import *
from NetworkingModule.Networking import *
from NetworkingModule.Message import *


class FunctionalTestInteraction(object):

    def __init__(self, port):
        self.networking = Networking('127.0.0.1', int(port))
        print('Started interaction with functional tests on port:' + str(port))
        self.update()

    def update(self):
        if not AllowingProcessing().allow_processing:
            return 0

        update_timeout = 0.1

        for message in self.networking.get_messages('func_testing', True):
            if len(message.data.split(None, 1)) == 1:
                arguments = ''
            else:
                arguments = message.data.split(None, 1)[1]

            self.networking.send_message(Message(message.peer, prefix='func_testing', text=Interface.execute_command(
                message.data.split(None, 1)[0],
                arguments
            )))

        timer = Timer(update_timeout, self.update)
        timer.start()
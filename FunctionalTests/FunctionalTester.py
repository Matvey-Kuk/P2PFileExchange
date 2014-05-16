from time import sleep
import argparse

from FunctionalTests.Instance import *
from FunctionalTests.NetworkingModule.Networking import *
from FunctionalTests.NetworkingModule.Message import *

parser = argparse.ArgumentParser(description='Hello, p2p world.')
parser.add_argument('-path', '-p', dest='path', help='Test program path')

networking = Networking('127.0.0.1', 1234)


instance = Instance(
    parser.parse_args().path + '/Main.py',
    ' -port 1235 -P2PModule -UsersDatabaseModule -functionalTestInteractionPort 1111'
)
networking.provoke_connection('127.0.0.1', 1111)

for peer in networking.get_peers():
    networking.send_message(Message(peer, prefix='func_testing', text='auth register matvey'))

sleep(5)

for message in networking.get_messages('func_testing'):
    print(message.data)

print(instance.send_command('auth register matvey'))
instance.kill()

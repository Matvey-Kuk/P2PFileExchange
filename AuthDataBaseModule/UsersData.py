from CryptoModule.rsa import*


class UsersData(object):

    def __init__(self):
        self.nick_names = []
        self.pub_keys = []

    def new_peers(self):

import unittest

import rsa

from UsersDatabaseModule.Cryptography import *


class TestCryptography(unittest.TestCase):

    def setUp(self):
        pass

    def test_private_pub_keys(self):
        keys = Cryptography.generate_keys()
        message = 'Go left at the blue tree'
        signature = Cryptography.get_signature(message, keys['private_key'])
        self.assertTrue(Cryptography.verify_signature(message, keys['public_key'], signature))
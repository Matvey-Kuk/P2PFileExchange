import unittest

import rsa

from UsersDatabaseModule.Cryptography import *
from DatabaseEngineModule.Alteration import *


class TestCryptography(unittest.TestCase):

    def setUp(self):
        self.keys = Cryptography.generate_keys()

    def test_private_pub_keys(self):
        message = 'Go left at the blue tree'
        signature = Cryptography.get_signature(message, self.keys['private_key'])
        self.assertTrue(Cryptography.verify_signature(message, self.keys['public_key'], signature))

    def test_alteration_signing(self):
        test_alteration = Alteration({'Hello': 'World'}, VersionsRange(version=1))
        self.assertFalse(Cryptography.is_signed(test_alteration))

        test_alteration = Cryptography.sign_alteration(test_alteration, self.keys['private_key'])
        self.assertTrue(Cryptography.is_signed(test_alteration))


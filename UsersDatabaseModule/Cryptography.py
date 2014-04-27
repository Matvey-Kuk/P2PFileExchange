import rsa
from rsa import transform

from DatabaseEngineModule.Alteration import *


class Cryptography(object):

    @staticmethod
    def generate_keys():
        (public_key, private_key) = rsa.newkeys(512)
        return {
            'public_key': Cryptography.dump_public_key(public_key),
            'private_key': Cryptography.dump_private_key(private_key)
        }

    @staticmethod
    def get_signature(data, private_key):
        return transform.bytes2int(
            rsa.sign(Cryptography.encode_data(data), Cryptography.restore_private_key(private_key), 'MD5')
        )

    @staticmethod
    def verify_signature(data, public_key, signature):
        return rsa.verify(
            Cryptography.encode_data(data),
            transform.int2bytes(signature),
            Cryptography.restore_public_key(public_key)
        )

    @staticmethod
    def encode_data(data):
        return str.encode(data)

    @staticmethod
    def dump_public_key(public_key):
        return {
            'n': public_key.n,
            'e': public_key.e
        }

    @staticmethod
    def dump_private_key(private_key):
        return {
            'n': private_key.n,
            'e': private_key.e,
            'd': private_key.d,
            'p': private_key.p,
            'q': private_key.q
        }

    @staticmethod
    def restore_public_key(public_key):
        return rsa.PublicKey(public_key['n'], public_key['e'])

    @staticmethod
    def restore_private_key(private_key):
        return rsa.PrivateKey(
            private_key['n'],
            private_key['e'],
            private_key['d'],
            private_key['p'],
            private_key['q']
        )
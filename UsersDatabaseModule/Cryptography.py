import rsa

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
        return rsa.sign(Cryptography.encode_data(data), Cryptography.restore_private_key(private_key), 'SHA-1')

    @staticmethod
    def verify_signature(data, public_key, signature):
        return rsa.verify(Cryptography.encode_data(data), signature, Cryptography.restore_public_key(public_key))

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

    @staticmethod
    def sign_alteration(alteration, private_key):
        new_changes = {}
        old_changes = alteration.get_changes()
        if not alteration.get_versions_range().get_size() == 1:
            raise Exception('Can sign only alteration with versions range size = 1.')
        for key in old_changes:
            new_changes[key] = {
                'data': old_changes[key],
                'signature': Cryptography.get_signature(old_changes[key], private_key)
            }
        return Alteration(
            changes=new_changes,
            versions_range=alteration.get_versions_range(),
            creation_time=alteration.get_creation_time()
        )



    @staticmethod
    def is_signed(alteration):
        signed = True
        changes = alteration.get_changes()
        for key in changes:
            if not ('signature' in changes[key] and 'data' in changes[key]):
                signed = False
        return signed
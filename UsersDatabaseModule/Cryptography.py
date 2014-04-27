import rsa


class Cryptography(object):

    @staticmethod
    def generate_keys():
        (public_key, private_key) = rsa.newkeys(1024)

        return {
            'public_key': public_key,
            'private_key': private_key
        }

    @staticmethod
    def get_signature(data, private_key):
        return rsa.sign(Cryptography.encode_data(data), private_key, 'SHA-1')

    @staticmethod
    def verify_signature(data, public_key, signature):
        return rsa.verify(Cryptography.encode_data(data), signature, public_key)

    @staticmethod
    def encode_data(data):
        return str.encode(data)
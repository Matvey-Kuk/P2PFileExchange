__author__ = 'Radmir'

import rsa

(pubkey, privkey) = rsa.newkeys(512)
# print(pubkey)
# print(privkey)
send_message = 'Ti kto takoy'
crypto = rsa.encrypt(send_message, pubkey)
reseive_message = rsa.decrypt(crypto, privkey)
# print(send_message,'\n',reseive_message)



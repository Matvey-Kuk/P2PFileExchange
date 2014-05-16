import rsa
(pubkey, privkey) = rsa.newkeys(512)
send_message = b'Ti kto takoy'
crypto = rsa.encrypt(send_message, pubkey)
reseive_message = rsa.decrypt(crypto, privkey)
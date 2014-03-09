__author__ = 'Radmir'

def encode_RSA(word,e,N):

    ret = []

    for v in word:

        n = ord(v)

        ret.append(int(n**e%N))
    return ret

def decode_RSA(word,d,N):

    ret = []

    for v in word:

        sim = v**d%N
        ret.append(unichr(sim))

    return ret
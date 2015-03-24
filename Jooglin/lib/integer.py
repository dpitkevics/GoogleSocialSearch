from hashids import Hashids


hashids = Hashids()


def num_encode(n):
    return hashids.encode(n)


def num_decode(s):
    return hashids.decode(s)[0]
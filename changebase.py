#!/usr/bin/env python
import math

"""
This is not as well-tested as it might appear at first glance.

Use at your own risk.
"""

def changebase(value, in_base, out_base):
    """
    >>> changebase([65], 10, 2)
    (1, 0, 0, 0, 0, 0, 1)
    >>> changebase((1,0,0,0,0,0,1), 2, 3)
    (2, 1, 0, 2)
    >>> changebase((2,1,0,2), 3, 10)
    (6, 5)
    >>> changebase([255], 256, 64)
    (3, 63)
    >>> changebase([64], 256, 64)
    (1, 0)
    >>> changebase([0], 256, 16)
    (0,)
    """
    v = sum(p*(in_base**i) for i, p in enumerate(reversed(list(value))))
    b = 0
    while (out_base**(b+1)) <= v:
        b += 1
    #b = int(math.floor(math.log(v, out_base))) # fails when value == 0
    res = []
    while b >= 0:
        res.append(v//(out_base**b))
        v %= (out_base**b)
        b -= 1
    assert v == 0, (value, in_base, out_base)
    return tuple(res)

class Alphabet(list):
    def index(self, v):
        try:
            return list.index(self, v)
        except ValueError:
            raise Exception("%r is not in this alphabet" % (v,))

    def encode_bytes(self, v):
        return "".join(map(self.__getitem__,changebase(map(ord,v),256,len(self))))

NB60 = Alphabet("0123456789ABCDEFGHJKLMNPQRSTUVWXYZ_abcdefghijkmnopqrstuvwxyz")
B64 = Alphabet("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")
encode_nb60 = lambda n: "".join(map(NB60.__getitem__, changebase(n, 10, 60)))
decode_nb60 = lambda s: "".join(map(str, changebase(map(NB60.index, s), 60, 10)))

B58 = Alphabet("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")

def encode_base58(v):
    """
    tests from go-base58

    encodes bytes into a bitcoin-style base58 string (?)

    >>> encode_base58(bytes((97,)))
    '2g'
    >>> encode_base58(bytes.fromhex("73696d706c792061206c6f6e6720737472696e67"))
    '2cFupjhnEsSn59qHXstmK2ffpLv2'
    >>> encode_base58(bytes.fromhex("00eb15231dfceb60925886b67d065299925915aeb172c06647"))
    '1NS17iag9jJgTHD1VXjvLCEnZuQ3rJDE9L'
    >>> encode_base58(b'')
    ''
    >>> encode_base58(b' ')
    'Z'
    >>> encode_base58(b'-')
    'n'
    >>> encode_base58(b'0')
    'q'
    >>> encode_base58(b'1')
    'r'
    >>> encode_base58(b'-1')
    '4SU'
    >>> encode_base58(b'11')
    '4k8'
    >>> encode_base58(b'abc')
    'ZiCa'
    >>> encode_base58(b'1234598760')
    '3mJr7AoUXx2Wqd'
    >>> encode_base58(b'abcdefghijklmnopqrstuvwxyz')
    '3yxU3u1igY8WkgtjK92fbJQCd4BZiiT1v25f'
    >>> encode_base58(b'00000000000000000000000000000000000000000000000000000000000000')
    '3sN2THZeE9Eh9eYrwkvZqNstbHGvrxSAM7gXUXvyFQP8XvQLUqNCS27icwUeDT7ckHm4FUHM2mTVh1vbLmk7y'
    """
    prefix = ''
    while v.startswith(b'\0'):
        prefix += B58[0]
        v = v[1:]
    if v:
        return prefix + "".join(map(B58.__getitem__,changebase(v,256,58)))
    else:
        return prefix

def decode_base58(v):
    """
    decodes a bitcoin-style base58 string into bytes (?)

    >>> decode_base58('2g') == bytes([97])
    True
    >>> decode_base58('')
    b''
    >>> decode_base58('Z')
    b' '
    >>> decode_base58('n')
    b'-'
    >>> decode_base58('q')
    b'0'
    >>> decode_base58('r')
    b'1'
    >>> decode_base58('4SU')
    b'-1'
    >>> decode_base58('4k8')
    b'11'
    >>> decode_base58('ZiCa')
    b'abc'
    >>> decode_base58('3mJr7AoUXx2Wqd')
    b'1234598760'
    >>> decode_base58('3yxU3u1igY8WkgtjK92fbJQCd4BZiiT1v25f')
    b'abcdefghijklmnopqrstuvwxyz'
    >>> decode_base58('3sN2THZeE9Eh9eYrwkvZqNstbHGvrxSAM7gXUXvyFQP8XvQLUqNCS27icwUeDT7ckHm4FUHM2mTVh1vbLmk7y')
    b'00000000000000000000000000000000000000000000000000000000000000'
    >>> for i in range(2**8):
    ...     for j in range(2**8):
    ...         s = bytes([i]) + bytes([j])
    ...         assert decode_base58(encode_base58(s)) == s,\
                       (repr(s), encode_base58(s), decode_base58(encode_base58(s)))
    >>> decode_base58("Hello")
    Traceback (most recent call last):
    Exception: 'l' is not in this alphabet
    """
    prefix = b''
    while v.startswith(B58[0]):
        prefix += b'\0' 
        v = v[1:]
    if v:
        return prefix + bytes(changebase(map(B58.index,v),58,256))
    else:
        return prefix

if __name__ == "__main__":
    import doctest
    print(doctest.testmod())


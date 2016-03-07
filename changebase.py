#!/usr/bin/env python

def changebase(value, in_base, out_base):
    """
    >>> changebase(65, 10, 2)
    (1, 0, 0, 0, 0, 0, 1)
    >>> changebase((1,0,0,0,0,0,1), 2, 3)
    (2, 1, 0, 2)
    >>> changebase((2,1,0,2), 3, 10)
    (6, 5)
    """
    assert value >= 0, value
    if in_base == 10 and type(value) in (int,long):
        v = value
    else:
        v = sum(p*(in_base**i) for i, p in enumerate(reversed(value)))
    b = 0
    while (out_base**(b+1)) <= v:
        b += 1
    res = []
    while b >= 0:
        res.append(v/(out_base**b))
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

NB60 = Alphabet("0123456789ABCDEFGHJKLMNPQRSTUVWXYZ_abcdefghijkmnopqrstuvwxyz")

encode_nb60 = lambda n: "".join(map(NB60.__getitem__, changebase(n, 10, 60)))
decode_nb60 = lambda s: "".join(map(str, changebase(map(NB60.index, s), 60, 10)))

B58 = Alphabet("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")

def encode_base58(v):
    """
    tests from go-base58
    >>> encode_base58(chr(97))
    '2g'
    >>> encode_base58("73696d706c792061206c6f6e6720737472696e67".decode("hex"))
    '2cFupjhnEsSn59qHXstmK2ffpLv2'
    >>> encode_base58("00eb15231dfceb60925886b67d065299925915aeb172c06647".decode("hex"))
    '1NS17iag9jJgTHD1VXjvLCEnZuQ3rJDE9L'
    >>> encode_base58('')
    ''
    >>> encode_base58(' ')
    'Z'
    >>> encode_base58('-')
    'n'
    >>> encode_base58('0')
    'q'
    >>> encode_base58('1')
    'r'
    >>> encode_base58('-1')
    '4SU'
    >>> encode_base58('11')
    '4k8'
    >>> encode_base58('abc')
    'ZiCa'
    >>> encode_base58('1234598760')
    '3mJr7AoUXx2Wqd'
    >>> encode_base58('abcdefghijklmnopqrstuvwxyz')
    '3yxU3u1igY8WkgtjK92fbJQCd4BZiiT1v25f'
    >>> encode_base58('00000000000000000000000000000000000000000000000000000000000000')
    '3sN2THZeE9Eh9eYrwkvZqNstbHGvrxSAM7gXUXvyFQP8XvQLUqNCS27icwUeDT7ckHm4FUHM2mTVh1vbLmk7y'
    """
    prefix = ''
    while v.startswith(chr(0)):
        prefix += B58[0]
        v = v[1:]
    if v:
        return prefix + "".join(map(B58.__getitem__,changebase(map(ord,v),256,58)))
    else:
        return prefix

def decode_base58(v):
    """
    >>> decode_base58('2g') == chr(97)
    True
    >>> decode_base58('')
    ''
    >>> decode_base58('Z')
    ' '
    >>> decode_base58('n')
    '-'
    >>> decode_base58('q')
    '0'
    >>> decode_base58('r')
    '1'
    >>> decode_base58('4SU')
    '-1'
    >>> decode_base58('4k8')
    '11'
    >>> decode_base58('ZiCa')
    'abc'
    >>> decode_base58('3mJr7AoUXx2Wqd')
    '1234598760'
    >>> decode_base58('3yxU3u1igY8WkgtjK92fbJQCd4BZiiT1v25f')
    'abcdefghijklmnopqrstuvwxyz'
    >>> decode_base58('3sN2THZeE9Eh9eYrwkvZqNstbHGvrxSAM7gXUXvyFQP8XvQLUqNCS27icwUeDT7ckHm4FUHM2mTVh1vbLmk7y')
    '00000000000000000000000000000000000000000000000000000000000000'
    >>> for i in range(2**8):
    ...     for j in range(2**8):
    ...         s = chr(i) + chr(j)
    ...         assert decode_base58(encode_base58(s)) == s,\
                       (repr(s), encode_base58(s), decode_base58(encode_base58(s)))
    >>> decode_base58("Hello")
    Traceback (most recent call last):
    Exception: 'l' is not in this alphabet
    """
    prefix = ''
    while v.startswith(B58[0]):
        prefix += chr(0)
        v = v[1:]
    if v:
        return prefix + ''.join(map(chr,changebase(map(B58.index,v),58,256)))
    else:
        return prefix

if __name__ == "__main__":
    import doctest
    print doctest.testmod()


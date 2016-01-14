#!/usr/bin/env python
import sys

# "The primality of the number has been rigorously proven" - RFC 2412
oakley2 = int("""
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE65381
FFFFFFFF FFFFFFFF
""".replace(' ','').replace('\n','').replace('\t',''), 16)

smallprime=127

def toydh(a,b=None,p=smallprime):
    """
    >>> from random import randrange
    >>> alice_private = randrange(1, oakley2)
    >>> alice_public  = toydh(alice_private, )
    >>> bob_private   = randrange(1, oakley2)
    >>> bob_public    = toydh(bob_private)
    >>> toydh(alice_public, bob_private) == toydh(bob_public, alice_private)
    True
    """
    if b is None:
        return pow(2, a%p, p)
    else:
        return pow(a%p, b%p, p)

def residues(p):
    """
    >>> residues(127)
    [1, 2, 4, 8, 16, 32, 64]
    >>> len(residues(47))
    23
    """
    return sorted(set(toydh(i, None, p) for i in range(p)))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        import doctest
        print doctest.testmod()
    else:
        print toydh(*map(int,sys.argv[1:]))

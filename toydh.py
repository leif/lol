#!/usr/bin/env python
import sys

"""
playing around with diffie-hellman

watch out, there is some very confused stuff here
"""

# "The primality of the number has been rigorously proven" - RFC 2412
# "Oakley Group 2" 1024-bit safe prime from RFC2412
oakley2_p = int("""
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE65381
FFFFFFFF FFFFFFFF
""".replace(' ','').replace('\n','').replace('\t',''), 16)

oakley2_q = int("""
7FFFFFFF FFFFFFFF E487ED51 10B4611A 62633145 C06E0E68
94812704 4533E63A 0105DF53 1D89CD91 28A5043C C71A026E
F7CA8CD9 E69D218D 98158536 F92F8A1B A7F09AB6 B6A8E122
F242DABB 312F3F63 7A262174 D31BF6B5 85FFAE5B 7A035BF6
F71C35FD AD44CFD2 D74F9208 BE258FF3 24943328 F67329C0
FFFFFFFF FFFFFFFF
""".replace(' ','').replace('\n','').replace('\t',''), 16)


# 1536-bit prime from RFC3526 (via obfs3_dh.py)
rfc3526_p = int("""
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA237327 FFFFFFFF FFFFFFFF""".replace(' ','').replace('\n','').replace('\t',''), 16)

rfc3526_q = (rfc3526_p-1)//2

# oakley2_p is a safe prime and oakley2_q is its sophie-germain prime
assert oakley2_q*2 + 1 == oakley2_p

small_p=127
small_q=7

def toydh(a,b=None,p=small_p):
    """
    >>> from random import randrange
    >>> order = len(residues(small_p)); order
    63
    >>> alice_private = randrange(order)
    >>> alice_public  = toydh(alice_private)
    >>> bob_private   = randrange(order)
    >>> bob_public    = toydh(bob_private)
    >>> toydh(alice_public, bob_private) == toydh(bob_public, alice_private)
    True
    >>> blind = randrange(small_p)
    >>> alice_public_blinded = toydh(alice_public, blind)
    >>> alice_private_blinded = (blind * alice_private) % order
    >>> toydh(bob_public, alice_private_blinded) == toydh(alice_public_blinded, bob_private)
    True
    """
    if b is None:
        return pow(2, a%p, p)
    else:
        return pow(a%p, b%p, p)


def test(g,p,q,a,b,z):
    """
    g = generator
    p = group order
    q = order of subgroup generated by g^x mod p
    a = alice secret
    b = bob secret
    z = blinding factor
    """
    # check params
    assert (p-1) % q == 0, (p,q)
    assert a < q
    assert b < q

    # make public keys
    A = pow(g,a,p)
    B = pow(g,b,p)

    # test unblinded DH
    assert pow(A,b,p) == pow(B,a,p), (g,p,q,a,b)

    # blind Alice's public key
    A_ = pow(A,z,p)

    # blind Alice's secret key
    a_ = (a*z) % q

    # test blinded DH
    assert pow(A_,b,p) == pow(B,a_,p), (g,p,q,a,b,z)

    # if both private keys are even, try fliping the public keys like
    # obfs3_dh.UniformDH does (this also works with smaller-order generators
    # so it does not mean the public keys are necessarily uniform)
    if (not a % 2) and (not b % 2):
        Au = p - A
        Bu = p - B
        assert pow(Au,b,p) == pow(B, a,p) ==\
               pow(A, b,p) == pow(Bu,a,p), (g,p,q,a,b)

def test_(p, q, gs, n):
    """
    >>> #gs=generators(127,7)
    >>> test_(127, 7, generators(127, 7), 7)
    >>> #test_(47, 23, generators(47, 23), 23)
    >>> test_(oakley2_p, oakley2_q, range(10), 10)
    >>> test_(rfc3526_p, rfc3526_q, [2], 10)
    """
    for g in gs:
        for a in range(n):
            for b in range(n):
                for z in range(n):
                    test(g,p,q,a,b,z)

def generators(p,q):
    """
    i forget wat made me write this part
    >>> gs = set(generators(127,7))
    >>> gs == set([2**i for i in range(1,7)])
    True
    """
    r = (p-1)//q
    return [pow(h,r,p) for h in range(2,p) if pow(h,r,p) != 1]

def residues(p):
    """

    >>> for p in primes(1000):
    ...     assert len(residues(p)) == (p-1)//2
    """
    return set(pow(i, 2, p) for i in range(1,(p+1)//2))

def primes(upperBound):
    """
    Returns a list of all prime numbers less than upperBound.
    >>> primes(50)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    """
    numbers = list(range(2, upperBound))
    primes = []
    while numbers:
        prime = numbers.pop(0)
        primes.append(prime)
        numbers = [n for n in numbers if n % prime]
    return primes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        import doctest
        print(doctest.testmod(verbose=0))
    else:
        print(toydh(*list(map(int,sys.argv[1:]))))

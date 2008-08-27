"Leif's notepad of higher-order functions"

import doctest
from itertools import groupby, count, islice, repeat, chain
from operator import add

# combinators, you never know when they'll come in handy
S,K,I = lambda x:lambda y:lambda z:x(z)(y(z)), lambda x:lambda y:x, lambda x:x
B,W,C = lambda x:lambda y:lambda z:x(y(z)), lambda x:lambda y:x(y)(y), \
        lambda x:lambda y:lambda z:x(z)(y)
Y = lambda f: (lambda x:f(lambda y:x(x)(y)))(lambda x:f(lambda y:x(x)(y)))
Y.__doc__ = " >>> uncurry(Y(mc(K)))(*range(5000)) and mc(K)(len)\n 5000"

# utilities

def ireduce(fn,seq,i=None):
    """reduce(f,s,i) <=> list(ireduce(f,s,i))[-1]
    Like the builtin reduce, but returns an iterator which returns each step.
    Sequence can be a non-terminating generator (eg, itertools.count):
    >>> fib = lambda n: list(islice(ireduce( lambda (a, b), i: (b, a+b),
    ...                                      count(), (0,1)), n,n+1))[0][0]
    >>> fib(0), fib(11)\n    (0, 89)"""
    cur = (i is not None and [i] or [seq.next()])[0]
    for next in seq:
        yield cur
        cur = fn(cur,next)
    yield cur

_ = lambda doc, fn: setattr(fn,'__doc__',str(doc)) or fn
_ = _("Set docstring attribute\n >>> _(1,lambda:0).__doc__\n '1'", _)

compose = _("Function composition\n   compose(a,b,c)(d,e) -> a(b(c(d,e)))",
    lambda *f: lambda *a: reduce(lambda p, fn: [fn(*p)], reversed(f), a)[0] )

rcomp = lambda f: lambda *a: ireduce(lambda p,fn: [fn(*p)], f, a)

ncomp = _("""Compose function with itself n times
    ncomp(f)(3)(x) -> f(f(f(x)))
    >>> ncomp(lambda i:i+1)(1005)(42)\n    1047
    >>> fib = lambda n: ncomp(lambda (a,b)=(0,1):(b,a+b))(n)()[0]
    >>> fib(47),fib(1500)==fib(1499)+fib(1498)\n    (2971215073L, True)""",
    lambda f: lambda n: compose(*repeat(f,n)))

        
memoize = _("Memoization decorator", lambda f: (lambda d={}: lambda *a,**kw: \
    (lambda *k: d.setdefault(k, k in d or f(*a,**kw)))(tuple(kw.items()),a) )())

memo = _("Memoization, sans kwargs",
    lambda f: (lambda d={}: lambda *a: d.setdefault(a, a in d or f(*a)))())

mm=memo(memo)

countcalls = _("""Count calls to a function; return count when passed len
    >>> i=lambda n:n+1; ncomp(mc(i))(10)(1), mc(i)(len)
    (11, 10)""", lambda f: (lambda n=[0]: lambda *a,**kw:
        (len in a and n or n.__setitem__(0,n[0]+1) or [f(*a,**kw)])[0])())
mc=memo(countcalls)

uncurry = _("(a -> (b -> (c -> d))) -> (a, b, c) -> d",
    lambda f: lambda *a: reduce(lambda f,x: f(x), a, f))
ucgi = _("uncurry arguments through the getitem interface",
    lambda f: lambda *a: reduce(lambda f,x: f[x], a, f))

# recursive_fib = lambda n,(a,b)=(0,1): a if n==0 else recursive_fib(n-1,(b,a+b))
naive_fib = Y(lambda f: lambda n: n<2 and 1 or f(n-1)+f(n-2))

fib = lambda n: ncomp(lambda (a,b):(b,a+b))(n)([0,1])[0]
fib = _(""">>> fib(1500)
13551125668563101951636936867148408377786010712418497242133543153221487310873528750612259354035717265300373778814347320257699257082356550045349914102924249595997483982228699287527241931811325095099642447621242200209254439920196960465321438498305345893378932585393381539093549479296194800838145996187122583354898000L""", fib)

# 1-d cellular automata
wfr = _("""wfr(rule, current_state) -> next_state
Transition a one-dimensional binary cellular automaton.
The rule is a Wolfram code; the state is a list of ones and zeros.""",
    lambda w,s:[w>>(s[i-1]*4+s[i]*2+s[(i+1)%len(s)])&1 for i in range(len(s))])
r110 = lambda s: wfr(110,s)
r110n = _("""Compute n generations of rule 110
    >>> r110n(7)([0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
    [0, 1, 1, 0, 1, 0, 1, 1, 1, 0]""", ncomp(r110))

if __name__=='__main__': doctest.testmod()

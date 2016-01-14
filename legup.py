#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a thing I began on 2016-01-13 while trying to learn about quadratic
residues (while trying to learn about the Decisional Diffie–Hellman assumption
(while trying to learn about [...])).

I started writing this because I wanted to see a visualization of the Legendre
symbol, but after working on it for several hours I got a bit distracted and
ended up also making text-based visualizations of a few other functions
involving primes.  I think "lightshow4" might be my favorite. (Make your
terminal window at least 190 columns wide before running it, or specify a
smaller width after the function name.)

The interesting features in many of these plots aren't visible until you get a
bit larger, so zooming your terminal to a very small text size and maximizing
the window is recommended. Maybe I'll revisit this project sometime and make
some actual graphics :)
"""

__author__ = "Leif Ryge <leif@synthesize.us>"

import math

try:
    from xtermcolor import colorize
except:
    def colorize(s,**k):
        return s

# copied from https://en.wikipedia.org/wiki/Legendre_symbol#Table_of_values
wikipedia_text="""
eJzFV0FSwzAMvOsVeYJlN3XyF37ADO/gzBN5CZvQKRBb0rrt0IPaSbyW1qu1Cm/Ty/Q6TZMiMqIg
TogZcUZUxIJYN0xCAKgAKoAKoAKoACqACqACmIHLwGXgMnAZuAxcBi4Dl4HLwJUk5VL68/0DX+m5
TzL/ef7+3J7Ts95Lvaz8rB5x6X8RonrEaYf9MUtqsj92l+x+bKBt8t5624KH7Jf9TriyRtVaRnGr
wpyy3dGe3VqBoyq9WpaZ3eySC8fBymyrZrFOU1RR8g1C9YlwqH7ug8mkdA3IZbEF8ncw55FSmW6N
k2TXjNbIKRCMFyCWb8SBu2inEsnkkzweesRjPrFqJfbKjVjLOpzVI5lDrbyi4xqwg0fmdaQ0owGv
dm9dzgPnZZNGVmesL+c6ssUnzbY48p/UcINXinMfo+D+XuodP4XMzffFdHpX1/iOxtTHOmWT3ikt
4Z99diHunnNj7Rqy3CES2xm++7+kWt15zk1g7pL7GRtimrbXvkacz6OD2Dbr5AOvcuVlH4FzFFc5
5A9O9aDViIO81vPt7E8tTavBzN/NTFPWFb0z4h/W29po24eTyvc/eOVK8AqyuBaPx0+n0hd7ngjY
""".decode('base64').decode('zip').replace('\xe2\x88\x92','-').split('\n')[1:]

# parse wikipedia text into matrix, and add a zero column
wikipedia_matrix = [ [0] + map(int, r.split()[1:]) for r in wikipedia_text ]

def render_matrix(m, pallete=None, ticks=False, color=False, minValue=-1, maxValue=1, ticks_x_offset=0):
    """
    >>> print render_matrix(wikipedia_matrix),
    _X _X _X _X _X _X _X _X _X _X _
    _X  X_X  X_X  X_X  X_X  X_X  X_
    _XX X  _XX X  _XX X  _XX X  _XX
    _X XXX   X _X XXX   X _X XXX   
    _X XX    XX X_X XX    XX X_X XX
    _XX X   XX   X XX_XX X   XX   X
    _X  XXXX X X    XX _X  XXXX X X
    _XXXX X XX  XX  X X    _XXXX X 
    _X  XXXX X   X  X   X XXXX  X_X
    _XX XX XXXX   X X XXX    X  X  
    _X XX  X XXXX   X    X   XXXX X
    _XX XX  XXX     X X XX X X     
    _X  X X  XXX XXXXX   X XXX     
    _XXXX XXXX  X X XXX  X  XX XX  
    _X  X XX XXX X XXX      XX  XX 
    _X XXX X X  X  XXX XXXX  XXXXX 
    _X XXX   X  XXXXX  XX X  X X   
    _X  X X  XX   XXXX X XXXXXX  X 
    _XXXXXX XXX X  XX XXX   XX X XX
    _XXXX X XX  X   X XX   XXX X   
    _XX XX  XXXX X  X XXXXXX XX    
    _X XX  X XXXX   XX   X X XXXXXX
    _XX XX  XXXX    XXX XXX  X     
    _XXXX X XX XX   X X   X XX X   
    _X  XXX  X   XX XX XXXXXXX    X
    _XX X  XXX   XXXXXXX   X XX XXX
    _X XX    XXXXXX X  X   X X X XX
    _X XXX X X  X  XX   XXX  XXXXX 
    _XX X  XXX X XXXX X   X  XX X X
    _XX X   XX X X XXXXX XX  XX   X
    """
    if pallete is None:
        pallete=" _X"
    return "\n".join(
        ([render_ticks(len(m[0])-1, ticks, ticks_x_offset)] if ticks else [])+
        [ "".join(c(i-minValue,maxValue-minValue,pallete,color)
          for i in r[:-1 if ticks else len(r)])+(' %s' % (r[-1],) if ticks else '') for r in m] )

def c(v, v_max, pallete=" \\#", color=0):
    if color:
        bg = int((v/float(v_max))*((2**24)-1))
        fg = (bg + int(color,16)) % ((2**24)-1)
        return colorize(pallete[v], rgb=fg, bg=bg)
    else:
        return pallete[v]

def render_ticks(w, base=2, x_offset=0, y_offset=0, pallete="| "):
    """
    >>> print render_ticks(15)
    |||||||||||||||   1
    | | | | | | | | - 2
    |   |   |   |   - 4
    |       |       - 8
    >>> print render_ticks(16)
    |||||||||||||||| - 1
    | | | | | | | |  - 2
    |   |   |   |    - 4
    |       |        - 8
    >>> print render_ticks(17)
    |||||||||||||||||   1
    | | | | | | | | |   2
    |   |   |   |   |   4
    |       |       |   8
    |               | - 16
    >>> print render_ticks(18)
    |||||||||||||||||| - 1
    | | | | | | | | |    2
    |   |   |   |   |    4
    |       |       |    8
    |               |  - 16
    >>> print render_ticks(18, 3)
    |||||||||||||||||| 1
    |  |  |  |  |  |   3
    |        |         9
    >>> print render_ticks(18, 3, 4)
    |||||||||||||||||| 1
      |  |  |  |  |  | 3
         |        |    9
    >>> print render_ticks(60, math.e/2, 0, 1)
    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 1.35914091423
    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 1.84726402473
    | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  2.5106921154
    |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |   3.41238437707
    |   |   |   |   |   |   |   |   |   |   |   |   |   |   |    4.63791122196
    |     |     |     |     |     |     |     |     |     |      6.30357489832
    |       |       |       |       |       |       |       |    8.56744655022
    |          |          |          |          |          |     11.6443671369
    |              |              |              |               15.826335796
    |                    |                    |                  21.5102205027
    |                            |                            |  29.2354207594
    |                                      |                     39.7350564988
    |                                                     |      54.0055410167
    """
    w += x_offset
    return "\n".join(
        "%s %s"%("".join(pallete[bool(x%int(base**y))]
                         for x in range(x_offset, w)),
                 (base**y if base != 2
                          else "%s %s"%(" -"[((w-1)&(base**y))>>y], base**y)))
        for y in range(y_offset, int(math.ceil(math.log(w, base)))))

def create_leg_matrix(w, h, x_offset=0, op=0, ticks=0):
    """
    >>> create_leg_matrix(31, 128) == wikipedia_matrix
    True
    """
    return [[calculateLegendre(a+x_offset,p) for a in range(w)]+([p] if ticks else []) for p in range(3, h) if op or isPrime(p)]


def render_legendre(max_a=76, max_p=62, pallete=" #_", ticks=2, x_offset=0, op=0, color=0):
    """
    >>> print render_legendre(72, 83)
    |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| - 1
    | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |  - 2
    |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |    - 4
    |       |       |       |       |       |       |       |       |          8
    |               |               |               |               |          16
    |                               |                               |          32
    |                                                               |        - 64
    #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_ #_  3
    #_  _#_  _#_  _#_  _#_  _#_  _#_  _#_  _#_  _#_  _#_  _#_  _#_  _#_  _#_ 5
    #__ _  #__ _  #__ _  #__ _  #__ _  #__ _  #__ _  #__ _  #__ _  #__ _  #_ 7
    #_ ___   _ #_ ___   _ #_ ___   _ #_ ___   _ #_ ___   _ #_ ___   _ #_ ___ 11
    #_ __    __ _#_ __    __ _#_ __    __ _#_ __    __ _#_ __    __ _#_ __   13
    #__ _   __   _ __#__ _   __   _ __#__ _   __   _ __#__ _   __   _ __#__  17
    #_  ____ _ _    __ #_  ____ _ _    __ #_  ____ _ _    __ #_  ____ _ _    19
    #____ _ __  __  _ _    #____ _ __  __  _ _    #____ _ __  __  _ _    #__ 23
    #_  ____ _   _  _   _ ____  _#_  ____ _   _  _   _ ____  _#_  ____ _   _ 29
    #__ __ ____   _ _ ___    _  _  #__ __ ____   _ _ ___    _  _  #__ __ ___ 31
    #_ __  _ ____   _    _   ____ _  __ _#_ __  _ ____   _    _   ____ _  __ 37
    #__ __  ___     _ _ __ _ _     ___  __ __#__ __  ___     _ _ __ _ _      41
    #_  _ _  ___ _____   _ ___     _   __ _ __ #_  _ _  ___ _____   _ ___    43
    #____ ____  _ _ ___  _  __ __   _ _ __    _    #____ ____  _ _ ___  _  _ 47
    #_  _ __ ___ _ ___      __  __      ___ _ ___ __ _  _#_  _ __ ___ _ ___  53
    #_ ___ _ _  _  ___ ____  _____     __    _   __ __ _ _   _ #_ ___ _ _  _ 59
    #_ ___   _  _____  __ _  _ _      _ _  _ __  _____  _   ___ _#_ ___   _  61
    #_  _ _  __   ____ _ ______  _   _ ___ __      _ _    ___  __ _ __ #_  _ 67
    #______ ___ _  __ ___   __ _ __ _   ___ _  _ _  ___   _  __ _   _      # 71
    #____ _ __  _   _ __   ___ _    _  ____  _    _ ___   __ _   _  __ _ ___ 73
    #__ __  ____ _  _ ______ __    __   _ _ _ _ ___  ____  _      _ __ _     79
    """
    return render_matrix(create_leg_matrix(max_a, max_p, x_offset, op, ticks), pallete, ticks, color)


class MThoma:

    # this stuff is from http://martin-thoma.com/calculate-legendre-symbol/

    @staticmethod
    def isPrime(a):
        # lol
        return all(a % i for i in xrange(2, a))

    # http://stackoverflow.com/a/14793082/562769
    @staticmethod
    def factorize(n):
        factors = []

        p = 2
        while True:
            while(n % p == 0 and n > 0): #while we can divide by smaller number, do so
                factors.append(p)
                n = n / p
            p += 1  #p is not necessary prime, but n%p == 0 only for prime numbers
            if p > n / p:
                break
        if n > 1:
            factors.append(n)
        return factors

    @staticmethod
    def calculateLegendre(a, p):
        """
       Calculate the legendre symbol (a, p) with p is prime.
       The result is either -1, 0 or 1

       >>> calculateLegendre(3, 29)
       -1
       >>> calculateLegendre(111, 41) # Beispiel aus dem Skript, S. 114
       -1
       >>> calculateLegendre(113, 41) # Beispiel aus dem Skript, S. 114
       1
       >>> calculateLegendre(2, 31)
       1
       >>> calculateLegendre(5, 31)
       1
       >>> calculateLegendre(150, 1009) # http://math.stackexchange.com/q/221223/6876
       1
       >>> calculateLegendre(25, 1009) # http://math.stackexchange.com/q/221223/6876
       1
       >>> calculateLegendre(2, 1009) # http://math.stackexchange.com/q/221223/6876
       1
       >>> calculateLegendre(3, 1009) # http://math.stackexchange.com/q/221223/6876
       1
       """
        if a >= p or a < 0:
            return calculateLegendre(a % p, p)
        elif a == 0 or a == 1:
            return a
        elif a == 2:
            if p%8 == 1 or p%8 == 7:
                return 1
            else:
                return -1
        elif a == p-1:
            if p%4 == 1:
                return 1
            else:
                return -1
        elif not isPrime(a):
            factors = factorize(a)
            product = 1
            for pi in factors:
                product *= calculateLegendre(pi, p)
            return product
        else:
            if ((p-1)/2)%2==0 or ((a-1)/2)%2==0:
                return calculateLegendre(p, a)
            else:
                return (-1)*calculateLegendre(p, a)

globals().update(dict((k, getattr(MThoma,k)) for k in MThoma.__dict__ if '_' not in k))

def render_primes(w=120, pallete=' #', ticks=2, color=0):
    m = [ [0 if not (isPrime(x)) else 1 for x in range(w)] + (['<--primes'] if ticks else []) ]
    return render_matrix(m, pallete=pallete, ticks=ticks, minValue=0, maxValue=1, color=color)

CL = "\x1b[H"

def lightshow1(w=180, h=60, n=0, pallete=' #', ticks=0, color=0):
    while True:
        n+=1
        m = [ [isPrime((x+n)%(5+y)) for x in range(w)] for y in range(h) ]
        print CL + render_matrix(m, pallete=pallete, ticks=ticks, minValue=0, maxValue=1, color=color)
        print n

def lightshow1(w=180, h=60, n=0, pallete=' #', ticks=0, color=0):
    while True:
        n+=1
        m = [ [isPrime((x+n)%(5+y)) for x in range(w)] for y in range(h) ]
        print CL + render_matrix(m, pallete=pallete, ticks=ticks, minValue=0, maxValue=1, color=color)
        print n

def lightshow2(w=180, h=60, n=0, pallete=' #', ticks=0, color=0):
    while True:
        n+=1
        m = [ [isPrime((x+n**2)%(1+y)) for x in range(w)] for y in range(h) ]
        print CL + render_matrix(m, pallete=pallete, ticks=ticks, minValue=0, maxValue=1, color=color)
        print n

def lightshow3(w=180, h=60, n=0, pallete=' #_|', ticks=0, color=0):
    while True:
        n+=1
        m = [ [isPrime((x+n)%(1+abs(y-int((1+math.sin(n/40.0))*30)))) for x in range(w)] for y in range(h) ]
        print CL + render_matrix(m, pallete=pallete, ticks=ticks, minValue=0, maxValue=3, color=color)
        print n

osc = lambda z, n: (abs((-z*((n/z)%2)) + (n%z)))

def lightshow3a(w=180, h=60, n=0, pallete=' #_|', ticks=0, color=0):
    while True:
        n+=1
        m = [ [isPrime((x+n)%(1+abs(y-osc(60,n) ))) for x in range(w)] for y in range(h) ]
        print CL + render_matrix(m, pallete=pallete, ticks=ticks, minValue=0, maxValue=3, color=color)
        print n

def lightshow4(w=180, h=60, n=0, pallete=' #', ticks=0, color=0):
    while True:
        n+=1
        z=60
        m = [ [isPrime((x+( (10+ osc(z,n) ) **2))%(10+y)) for x in range(w)] for y in range(h) ]
        print CL + render_matrix(m, pallete=pallete, ticks=ticks, minValue=0, maxValue=1, color=color)
        print n, osc(z,n), n/20

def lightshow5(w=180, h=60, n=0, pallete=' #', ticks=0, color=0):
    while True:
        n+=1
        m = [ [isPrime((x+n*5)%(1+y)) for x in range(w)] for y in range(h) ]
        print CL + render_matrix(m, pallete=pallete, ticks=ticks, minValue=0, maxValue=1, color=color)
        print n

def lightshow6(w=180, start=1.08, stop=2, steps=1000):
    n=0
    while True:
        n+=1
        print CL + render_ticks(w, start + (stop-start)*(float(osc(steps,n))/steps))

def scroll_legendre(max_a=130, max_p=223, pallete=" #_", ticks=2, op=0, color=0):
    n=0
    while True:
        n+=1
        print CL + render_matrix(create_leg_matrix(max_a, max_p, n, op, ticks), pallete, ticks, color, -1, 1, n)

def test(verbose=0):
    import doctest
    return doctest.testmod(verbose=verbose)

def omghax(x):
    "¯\_(ツ)_/¯"
    try:
        return int(x)
    except:
        try:
            return float(x)
        except:
            return x

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        print "usage: %s <%s> [args]" % (sys.argv[0], "|".join(globals().keys()))
    else:
        print globals()[sys.argv[1]](*map(omghax,sys.argv[2:]))


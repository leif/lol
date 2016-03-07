#!/usr/bin/env python
import sys
import time
from random import choice
import itertools
from operator import itemgetter

def isascii(w):
    try:
        w.encode('ascii')
    except:
        return False
    return True

loadwords = lambda filename: set(
            map(str.lower,
                filter(lambda s: len(s) > 1,
                    filter(isascii,
                       file(filename).read().split()))))

words = loadwords('/usr/share/dict/words')

words |= set("a i racecar".split())

stripapo = lambda s: s.replace("'",'')

ispal = lambda s: s == rev(s)

#rev = lambda s: ''.join(reversed(s))
rev = lambda s: s[::-1]

r13 = dict( (w, w.encode('rot13')) for w in words )

r13words = dict( (k,v) for k,v in r13.items() if v in words )

palwords = set( w for w in words if w == rev(w) )

get_altpals = lambda words: dict( (w, rev(w)) for w in words if rev(w) in words )

altpals = get_altpals(words)
altpals2 = dict( (w, rev(stripapo(w))) for w in words if rev(stripapo(w)) in words )

duprev = lambda s: s+' '+rev(s)

randpal = lambda n: duprev(' '.join(choice(altpals.keys()) for i in range(n)))

def fd(delta):
    "from allmydata.util.time_format.format_delta"
    delta = int(delta)
    seconds = delta % 60
    delta  -= seconds
    minutes = (delta / 60) % 60
    delta  -= minutes * 60
    hours   = delta / (60*60) % 24
    delta  -= hours * 24
    days    = delta / (24*60*60)
    if not days:
        if not hours:
            if not minutes:
                return "%ss" % (seconds)
            else:
                return "%sm %ss" % (minutes, seconds)
        else:
            return "%sh %sm %ss" % (hours, minutes, seconds)
    else:
        return "%sd %sh %sm %ss" % (days, hours, minutes, seconds)

ft = lambda t: time.strftime("%c",time.gmtime(t))

laststatus = ''

def printline(*s):
    sys.stderr.write( "\x1b[K%s\n%s\x0d" % (' '.join(s), laststatus) )

def progressor(T, items="items"):
    i = 0
    start_time = time.time()
    txt = ''
    while i < T:
        i += 1
        if i % (T / 10000) == 0:
            p = (float(i) / T)
            now = time.time()
            sofar = now - start_time
            total_estimate = sofar / p
            remaining = total_estimate - sofar
            ips = int((i / sofar))
            global laststatus
            laststatus = "%.2f%% (%s til %s) [%s of %s] %d %s/s %s" % (
                     p*100, fd(remaining), ft(now+remaining),
                     fd(sofar), fd(total_estimate), ips, items, txt)
            sys.stderr.write( '\x1b[K%s\x0d' % (laststatus,) )
        txt = yield

def findpairs(func):
    def _f(words=words):
        pairs = {}
        T = len(words)
        p = progressor(T, "dicts")
        p.next()
        print "%s words in dictionary, ^2 = %s words" % (len(words), len(words)**2)
        found = 0
        for w1 in words:
            for w2 in words:
                if func(w1, w2):
                    found += 1
            p.send('found %s' % (found,))
    return _f

pairwords = set()
@findpairs
def findpairwords(w1, w2):
    if (w1 + w2) in words:
        printline(w1+ ' ' + w2)
        pairwords.add(w1 + ' ' + w2)
        return True

pairpals=dict()
@findpairs
def findpairpals(w1, w2):
    c = rev(w1 + w2)
    if c in words:
        pairpals[w1 + ' ' + w2] = c
        printline("%s / %s %s" % (c, w1, w2))
        return True

r13pairs = dict()
@findpairs
def find_r13pairs(w1, w2):
    c = (w1 + w2).encode('rot13')
    if c in words:
        printline("%s / %s %s" % (c, w1, w2))
        r13pairs[w1 + ' ' + w2] = c
        return True

def wordsquares(words=words, n=4, cur=()):
    """
    This returns all word squares of order n that can be made with a given set
    of words.

    See https://en.wikipedia.org/wiki/Word_square
    """
    if cur == ():
        words = [w for w in words if len(w) == n]
    d = len(cur)
    if d < n:
        for word in words:
            if word.startswith(''.join(map(itemgetter(d), cur))):
                for win in wordsquares(words, n, cur+(word,)):
                    yield win
    else:
        yield cur

def print_wordsquares(words=words, n=4):
    for sq in wordsquares(words, n):
        print "\n".join(sq+('--',))

def print_wordsquarepals(words=words, n=4):
    for sq in wordsquares(words, n):
        s = '\n'.join(sq)
        if s == rev(s):
            print s
            print '--'

def tiler( seq ):
    n = len(seq)
    m = len(seq[0])
    return (' '.join(seq[(x+y)%n][iy] for x in range(n)) for y in range(n) for iy in range(m))

def ptiler( seq ):
    NW = list(tiler(seq))
    NE = [rev(r) for r in NW]
    SW = rev(NW)
    SE = [rev(r) for r in SW]
    seq = [NW, NE, SW, SE]
    n = len(seq)
    m = len(seq[0])
    return (' '.join(seq[i+(j*(n/2))][iy] for i in range(n/2)) for j in range(n/2) for iy in range(m))

def spacer(n, seq):
    for i, x in enumerate(seq):
        if i > 0 and i%n ==0:
            yield ''
        yield x

def chr2color(c):
    v = (ord(c) - ord('a'))%26
    return int((2**24-1) *(v/25.0))

def addcolor(s):
    try:
        from xtermcolor import colorize
    except:
        return s
    return ''.join(
        colorize(c, rgb=0&chr2color(c)&~0x808080, bg=chr2color(c)|0xc0c0c0)
        if ord('a')<=ord(c)<=ord('z') else c for c in s)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print globals()[sys.argv[1]](*sys.argv[2:])
    else:
#        print_wordsquarepals(sorted(altpals), 4)
        n = 4
#        print "%s palindrome words" % (len(altpals),)
        words = [w for w in altpals if len(w) == n]
#        print "%s are %s chars" % (len(words), n)
        squares = list(wordsquares(words, n=4))
#        print "%s word squares of palindrome words" % (len(squares),)
        wsp = [s for s in squares if ispal(''.join(s))]
#        print "%s squares are themselves palindromic" % (len(wsp),)
        selection = [choice(wsp) for i in range(6)]
        grid = "\n".join(spacer(4, ptiler(selection)))
        print addcolor(grid)


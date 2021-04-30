#!/usr/bin/env python
import sys
import time
from random import choice, shuffle
import itertools
import codecs
from operator import itemgetter
def isascii(w):
    try:
        w.encode('ascii')
    except:
        return False
    return True

loadwords = lambda filename: set(
            map(str.lower,
                [s for s in list(filter(isascii,
                       open(filename).read().split())) if len(s) > 1]))

words = loadwords('/usr/share/dict/words')

words |= set("a i racecar".split())

stripapo = lambda s: s.replace("'",'')

ispal = lambda s: s == rev(s)

#rev = lambda s: ''.join(reversed(s))
rev = lambda s: s[::-1]

rot13 = lambda s: codecs.getencoder( "rot-13" )(s)[0]
r13 = dict( (w, rot13(w)) for w in words )

r13words = dict( (k,v) for k,v in list(r13.items()) if v in words )

palwords = set( w for w in words if w == rev(w) )

get_altpals = lambda words: dict( (w, rev(w)) for w in words if rev(w) in words )

altpals = get_altpals(words)
altpals2 = dict( (w, rev(stripapo(w))) for w in words if rev(stripapo(w)) in words )

duprev = lambda s: s+' '+rev(s)

randpal = lambda n: duprev(' '.join(choice(list(altpals.keys())) for i in range(n)))

def gnattang():
    """
    Print palindrome pairs that are eachothers rot13 encodings.

    With my dictionary, the only words of more than 2 characters are gnat/tang
    """
    for word in r13words:
        if rev(word) == r13words[word]:
            print("%s/%s" % (word, rev(word)))

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
        next(p)
        print("%s words in dictionary, ^2 = %s words" % (len(words), len(words)**2))
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
    c = rot13(w1 + w2)
    if c in words:
        printline("%s / %s %s" % (c, w1, w2))
        r13pairs[w1 + ' ' + w2] = c
        return True

itemgetter = lambda key: lambda value: value[key]

def wordsquares(words=words, n=4, cur=()):
    """
    This returns all word squares of order n that can be made with a given set
    of words.

    See https://en.wikipedia.org/wiki/Word_square
    """
    if cur == ():
        words = sorted([w for w in words if len(w) == n])
    d = len(cur)
    if d < n:
        for word in words:
            if word.startswith(''.join(map(itemgetter(d), cur))):
                for win in wordsquares(words, n, cur+(word,)):
                    yield win
    else:
        yield cur

def print_wordsquares(n=4, words=words):
    n=int(n)
    words = ['cyber'] + list(words)
    for sq in wordsquares(words, n):
        print("\n".join(sq+('--',)))

def print_wordsquarepals(words=altpals, n=4):
    "Prints the word squares that are palindromes"
    for sq in wordsquares(words, n):
        s = '\n'.join(sq)
        if ispal(s):
            print(s)
            print('--')

def tiler( seq ):
    n = len(seq)
    m = len(seq[0])
    return (' '.join(seq[(x+y)%n][iy] for x in range(n)) for y in range(n) for iy in range(m))

def ptiler( seq ):
    NW = list(seq)
    NE = [rev(r) for r in NW]
    SW = rev(NW)
    SE = [rev(r) for r in SW]
    seq = [NW, NE, SW, SE]
    n = len(seq)
    m = len(seq[0])
    return (' '.join(seq[i+(j*(n//2))][iy] for i in range(n//2)) for j in range(n//2) for iy in range(m))

def ptiler_n( n, seq ):
    for i in range(n):
        seq = ptiler(seq)
    return seq

def spacer(n, seq):
    for i, x in enumerate(seq):
        if i > 0 and i%n ==0:
            yield ''
        yield x

def chr2color(c):
    """
    make 26 colors and map characters into them such that "a" is black and "z"
    is white
    """
    v = (ord(c) - ord('a'))%26
    return int((2**24-1) *(v/25.0))

def addcolor(s):
    """
    adds ansi coloring to characters a-z
    """
    try:
        from xtermcolor import colorize
    except:
        return s
    return ''.join(
        colorize(c, rgb=0, bg=chr2color(c)|0xb0b0b0)
        #colorize(c, rgb=(chr2color(c)^(2**24-1)), bg=chr2color(c)|0xb0b0b0)
#        colorize(c, rgb=0xffffff, bg=chr2color(c)|0xb0b0b0)
        #colorize(c, rgb=chr2color(c)|0xb0b0b0, bg=chr2color(c)|0xb0b0b0)
        if ord('a')<=ord(c)<=ord('z') else c for c in s)

def colorpipe():
    for line in sys.stdin.readlines():
        sys.stdout.write(addcolor(line))
    return ""

def find_squares_of_unique_words(squares):
    """
    This finds a set of squares without duplicate words (in themselves OR in
    the set). It probably isn't the largest possible set of such squares, but
    it's one of them.
    """
    w2s = {}
    for square in squares:
        for word in square:
            w2s.setdefault(word, []).append(square)
    sorted_words = sorted(w2s, key=lambda w: len(w2s[w]))
    used = set()
    res = set()
    for word in sorted_words:
        for sq in w2s[word]:
            if len(sq) != len(set(sq)) or any(ow in used for ow in sq):
                continue
            res.add(sq)
            used |= set(sq)
            break
    return res

def find_more_squares_of_unique_words(squares):
    """
    This finds a set of squares without duplicate words (in themselves OR in
    the set). It probably isn't the largest possible set of such squares, but
    it's one of them. Maybe this finds more? (No, it seems to find a different
    set of the same size.)
    """
    w2s = {}
    for square in squares:
        for word in square:
            w2s.setdefault(word, []).append(square)
    sorted_words = sorted(w2s, key=lambda w: len(w2s[w]))
    used = set()
    res = set()
    for word in sorted_words:
        for sq in w2s[word]:
            if len(sq) != len(set(sq)) or any(ow in used for ow in sq):
                continue
            res.add(sq)
            used |= set(sq)
    missing_words = set(w2s.keys()) - used
    print("used %s, %s missing" % (len(used), len(missing_words)))
    sorted_words = list(missing_words) + sorted_words
    used = set()
    res = set()
    for word in sorted_words:
        for sq in w2s[word]:
            if len(sq) != len(set(sq)) or any(ow in used for ow in sq):
                continue
            res.add(sq)
            used |= set(sq)
    missing2 = set(w2s.keys()) - used
    print(set(missing_words) == set(missing2))
    print(missing_words)
    print(missing2)
    print(set(missing_words) ^ set(missing2))
    print("used %s, %s missing" % (len(used), len(missing_words)))
    return res

def test_find_more(n=4):
    squares = list(wordsquares(altpals, n=n))
    psquares = [s for s in squares if ispal(''.join(s))]
    upsquares = sorted(find_more_squares_of_unique_words(psquares))
    print("got %s squares" %(len(upsquares),))

def print_unique_palindromic_squares(n=4):
    """
    This prints a square consisting of palindromic squares of unique words.
    The super square itself is not palindromic, however.
    """
    n=int(n)
    squares = list(wordsquares(altpals, n=n))
    psquares = [s for s in squares if ispal(''.join(s))]
    upsquares = sorted(find_squares_of_unique_words(psquares))
    print("\n".join(spacer(n,tiler(upsquares))))

def palindromic_super_word_square(m=17, n=4):
    """
    This is what I call a palindromic super word square.
    * the entire square is a palindrome
    * each sub-square is a palindrome
    * each row and each column of characters are palindromes
    * each row and each column of sub-squares are word-unit palindromes
    * rows of sub-squares can be read as word-unit palindromes two different ways
    * assigning colors to each character produces nice results
    """
    n = int(n)
    m = int(m)
    print("%s palindromic words" % (len(altpals),))
    words = [w for w in altpals if len(w) == n]
    print("%s are %s chars" % (len(words), n))
    squares = list(wordsquares(words, n=4))
    print("%s word squares of palindromic words" % (len(squares),))
    wsp = [s for s in squares if ispal(''.join(s))]
    print("%s word squares of palindromes are themselves palindromic" % (len(wsp),))
    words_in_wsp = set([w for s in wsp for w in s])
    print("%s unique words in palindromic word squares" % (len(words_in_wsp),))
    unique_squares = list(find_squares_of_unique_words(wsp))
    print("%s squares of unique words" % (len(unique_squares),))
    print("here are %s random palindromic word squares forming a super palindromic word square" % (m,))
    #selection = [choice(wsp) for i in range(m)]
    shuffle(unique_squares)
    selection = unique_squares[:m]
    grid = "\n".join(spacer(n, ptiler(tiler(selection))))
    return addcolor(grid)

def print_one_nx(n=3):
    n=int(n)
    sq = choice(list(wordsquares(altpals)))
    print("\n".join(spacer(4,ptiler_n(n,sq))))

def nospace(f, *args):
    return globals()[f](*args).replace('\n\n','\n').replace(' ','')

def loop(cmd, *args):
    print("\x1b[H\x1b[2J", end=' ')
    while True:
        print("\x1b[H", end=' ')
        print(globals()[cmd](*args))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(globals()[sys.argv[1]](*sys.argv[2:]))
    else:
        print(palindromic_super_word_square())
#        print nspsws()


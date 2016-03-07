#!/usr/bin/env python
from random import randrange
from math import log

def birthday(bits, count):
    res = []

    for i in range(count):
        vs = set()
        while True:
            v = randrange(int(2**bits))
            if v in vs:
                break
            vs.add(v)
        res.append(len(vs))
    return res

mean = lambda seq: sum(seq) / float(len(seq))
median = lambda seq: sorted(seq)[len(seq)/2]
mode = lambda seq: sorted(seq, key=seq.count)[-1]
bitsize = lambda v: "%s (%.2f bits)" % (v, log(v, 2))
min, max = min, max # put these in globals() so report can use them below
report = lambda seq: "\n".join("%s: %s" % (f, bitsize(globals()[f](seq)))
                               for f in "mean median mode min max".split())

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print "usage: %s bits [count]"
    else:
        bits = float(sys.argv[1])
        count = 1000 if len(sys.argv) < 3 else int(sys.argv[2])
        print """
How many random %s-bit values (0 <= v < %s) do we need to pick before we get a
collission?  Lets try picking values until we get a collision (and saving the
count of values prior to the collision) %s times.

Results:""" % (bits, (2**bits), count)
        print report(birthday(bits, count))

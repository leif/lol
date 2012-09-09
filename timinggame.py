from time import time, sleep
from collections import deque

times  = 4
width  = 80
height = 24
levels = height-4

halfWidth = width / 2
data = dict((p, deque([],p)) for p in (2**b for b in range(levels)))
ratios = {}

prev = time()
i = 0
while True:
    i += 1
    now = time()
    delta = (now - prev) * times
    print "\x1b[H\x1b[2J"
    print "       :", "*" * halfWidth
    for period in sorted(data):
        datum = data[ period ]
        datum.append( delta )
        ratios[ period ] = sum(datum)/float(len(datum))
    for period in sorted(ratios):
        print "%8s %s" % (len(data[period]), "*" * int(halfWidth*ratios[period]))
    if tuple(set( int(halfWidth*r) for r in ratios.values() )) == (halfWidth,):
        print "WIN! took %s iterations!" % i
        break
    print " target:", "*" * halfWidth
    print "Instructions: hit the enter key, %s times per second" % times
    prev = now
    raw_input()

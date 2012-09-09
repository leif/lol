from sys import argv
from time import time, sleep
from collections import deque

times = 4  if len(argv) < 2 else int(argv[1])
lines = 20 if len(argv) < 3 else int(argv[2])
width = 50

data = dict((p, deque([],p)) for p in (2**b for b in range(lines)))
ratios = {}

prev = time()
i = 0
while True:
    i += 1
    now = time()
    delta = (now - prev) * times
    print "\x1b[H\x1b[2J"
    print "        ", "_" * width
    for period in sorted(data):
        datum = data[ period ]
        datum.append( delta )
        ratios[ period ] = sum(datum)/float(len(datum))
    for period in sorted(ratios):
        print "%8s %s" % (len(data[period]), "*" * int(width*ratios[period]))
    if tuple(set( int(width*r) for r in ratios.values() )) == (width,):
        print "WIN! score is %s" % i
        break
    print "        ", "^" * width
    print "Instructions: make all lines the correct length by hitting Enter %s times/second" % times
    prev = now
    raw_input()

from sys import argv
from time import time, sleep
from collections import deque
times = 4 if len(argv) < 2 else int(argv[1])
width = 4 if len(argv) < 3 else int(argv[2])
level = 1 if len(argv) < 4 else int(argv[3])
data  = [ deque([], 1) ]
start = time()
prev  = start
i     = 0
while True:
    now   = time()
    value = (now - prev) * times
    prev  = now
    clock = now - start
    print "\x1b[H\x1b[2J\x0d",
    print "Instructions: make all lines the correct length by hitting Enter %s times/second" % times
    print "       ", "_" * width
    means = []
    for period in data:
        period.append( value )
        mean = int(width * sum(period)/float(len(period)))
        means.append( mean )
        print "%7s %s" % (len(period), "=" * mean)
    if list(set( means )) == [width]:
        print "     :)", "!" * width
        level += 1
        width += 1
    else:
        print "       ", "^" * width
    if i > 0:
        seconds = clock % 60
        minutes = (clock - seconds)/60
        print "Level %s. After %dm %ds, cumulative mean is %.3f%% of target " % (level,minutes,seconds, 100*clock/i*times)
    i += 1
    bits = len( data )
    if len(data[-1]) == 2**(bits-1):
        data.append( deque( data[-1], 2**bits ) )
    raw_input()

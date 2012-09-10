from sys         import argv
from time        import time
from collections import deque
rate  = 4 if len(argv) < 2 else int(argv[1])
level = 4 if len(argv) < 3 else int(argv[2])
data  = [ deque([], 1) ]
start = time()
prev  = start - (1.0/rate)
i     = 0
while True:
    now    = time()
    clock  = now - start
    delta  = now - prev
    prev   = now
    if len(data[-1]) == 2**(len(data)-1): data.append(deque(data[-1], 2**len(data)))
    widths = []
    for window in data:
        window.append( delta )
        width = int(0.5+((level)*sum((delta*rate) for delta in window)/float(len(window))))
        widths.append( width )
    print "\x1b[H\x1b[2J\x0d",
    print "Instructions: make all lines the correct length by hitting Enter %s times/second" % rate
    if i>1 and list(set( widths[:level] )) == [ level ]:
        print ":)    |", "v" * level
        print "\n".join("%6s| %s" % (len(window), ">" * width) for window, width in zip(data[:level], widths))
        print ":)    |", "^" * level
        level += 1
    else:
        print "      |", "_" * level
        print "\n".join("%6s| %s" % (len(window), "=" * width) for window, width in zip(data[:level], widths))
        print "      |", "^" * level
    if i > 0:
        seconds = clock % 60
        minutes = (clock - seconds)/60
        print "Level %s. After %dm %ds, cumulative mean speed is %.3f%% of target" % (level,minutes,seconds, 100/(1.0/(i/clock/rate)))
    i += 1
    raw_input()

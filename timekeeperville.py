"timekeeperville is a game where you must keep time"
# by Leif Ryge, September 2012, WTFPL
from sys         import argv
from time        import time
from collections import deque
rate  = 4 if len(argv) < 2 else int(argv[1])
level = 4 if len(argv) < 3 else int(argv[2])
data  = [ deque([], 1) ]
start = time()
prev  = start - (1.0/rate)
while True:
    now     = time()
    clock   = now - start
    delta   = now - prev
    prev    = now
    seconds = clock % 60
    minutes = (clock - seconds)/60
    widths  = []
    if len(data[-1]) == 2**(len(data)-1): data.append(deque(data[-1], 2**len(data)))
    for window in data:
        window.append( delta )
        width = int(0.5+((level)*sum((delta*rate) for delta in window)/float(len(window))))
        widths.append( width )
    win = len(data) > 1 and list(set( widths[:level] )) == [ level ]
    print "\x1b[H\x1b[2J\x0d",
    print "Level %-3s|" % (level-3), "_v"[win] * level
    print "\n".join("%9s| %s" % (len(window),"=>"[win]*width) for window, width in zip(data[:level], widths))
    print "%3dm %2ds |" % (minutes, seconds), "^!"[win] * level
    print "Instructions: make all lines the correct length by hitting Enter %s times/second" % rate
    if win: level+=1
    raw_input()

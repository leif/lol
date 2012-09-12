"timekeeperville is a game where you must keep time"
# by Leif Ryge, September 2012, WTFPL
from time import time
from collections import deque
adj    = raw_input("Adjust settings? [yN] ")=="y"
rate   = int(adj and raw_input("Rate per second?    [default=4]  ") or 4)
level  = int(adj and raw_input("Starting level?     [default=1]  ") or 1)
limit  = int(adj and raw_input("Starting limit?     [default=15] ") or 15)
base   = int(adj and raw_input("Window size base?   [default=2]  ") or 2)
pause  = int(adj and raw_input("Inactivity timeout? [default=3]  ") or 3)
alt    = adj and raw_input("Alternate display mode? [yN] ") == "y" or 0
data   = [deque([], 1)]
widths = [level]
prev, clock, streak, best, score, left = 0, 0, 0, 0, 0, limit
while True:
    print "\x1b[H\x1b[2J\x0d",
    now   = time()
    delta = now - prev
    prev  = now
    if delta > pause:
        win = False
        print "Instructions: hit Enter %s times/second to keep all lines at correct length" % rate
    else:
        if len(data[-1]) == base**(len(data)-1): data.append(deque(data[-1], base**len(data)))
        for window in data: window.append( delta*rate )
        clock += delta
        widths = [ int(level*sum(window)/len(window)+0.5) for window in data[:level] ]
        win    = len(data)>1 and [level]==list(set(widths))
        streak = win and (left==limit and streak+1 or 1) or 0
        best   = max(streak, best)
        limit  = max(limit, level+best)
        left   = (left-delta, limit)[win]
        if win and left > 1: score+=left*streak
        print "Level %-3s|" % level, "=!"[win]*level, streak>1 and "%s streak!"%streak or win and ":)" or "too %s"%('slow','fast')[delta*rate<1]
    print "\n".join("%%9s| %%%ds"%(alt and level)%(len(window),"#>"[win]*width) for window,width in zip(data,widths))
    raw_input("%-6s%4s %s Score: %s \n"%("%d:%.2d"%(left/60,left%60),"[%s]"%best,"=!"[win]*level,score)) == "q" and exit()
    if left < 1: exit("Out of time! Played %dm%.2ds, taking %.1f seconds per level" % (clock/60,clock%60,clock/level))
    if win: level+=1

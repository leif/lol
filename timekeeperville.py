"timekeeperville is a game where you must keep time"
# by Leif Ryge, September 2012, WTFPL
from time import time
from collections import deque
adj    = "y" == raw_input("Adjust settings? [yN] ")
rate   = int(adj and raw_input("Rate per second?    [default=4] ") or 4)
level  = int(adj and raw_input("Starting level?     [default=1] ") or 1)
limit  = int(adj and raw_input("Starting limit?     [default=9] ") or 9)
base   = int(adj and raw_input("Window size base?   [default=2] ") or 2)
pause  = int(adj and raw_input("Inactivity timeout? [default=3] ") or 3)
alt    = adj and raw_input("Alternate display mode? [yN] ") == "y" or 0
data   = [deque([], 1)]
widths = [level]
prev, clock, last, streak, best = 0, 0, 0, 0, 0
while True:
    print "\x1b[H\x1b[2J\x0d",
    if len(data[-1]) == base**(len(data)-1): data.append(deque(data[-1], base**len(data)))
    now   = time()
    delta = now - prev
    prev  = now
    if delta > pause:
        win = False
        print "Instructions: hit Enter %s times/second to keep all lines at correct length" % rate
    else:
        widths = []
        for window in data:
            window.append( delta*rate )
            widths.append(int(level*sum(window)/len(window)+0.5))
        win    = len(data)>1 and [level]==list(set(widths[:level]))
        streak = win and (last==0 and streak+1 or 1) or 0
        best   = max(streak, best)
        limit  = max(limit, best*5)
        last   = (last+delta,0)[win]
        clock += delta
        print "Level %-3s|" % level, "=v"[win]*level, win and ":)" or "too %s"%('slow','fast')[delta*rate<1]
    print "\n".join("%%9s| %%%ds"%(alt and level)%(len(window),"#>"[win]*width) for window,width in zip(data[:level], widths))
    raw_input("%-6s%3d| %s %s "%("%d:%.2d"%((clock-clock%60)/60,clock%60),(limit-last),"^!"[win]*level,(best,"%s streak!"%streak)[1<streak])) == "q" and exit()
    if last > limit: exit("Out of time!")
    if win: level+=1

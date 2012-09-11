"timekeeperville is a game where you must keep time"
# by Leif Ryge, September 2012, WTFPL
from time import time
from collections import deque
ask    = "y" == raw_input("Adjust settings? [yN] ")
rate   = int(ask and raw_input("Rate per second?      [default=4] ") or 4)
level  = int(ask and raw_input("Starting level?       [default=1] ") or 1)
base   = int(ask and raw_input("Window size base?     [default=2] ") or 2)
pause  = int(ask and raw_input("Seconds before pause? [default=3] ") or 3)
data   = [deque([], 1)]
widths = [level]
prev   = 0
clock  = 0
while True:
    print "\x1b[H\x1b[2J\x0d",
    if len(data[-1]) == base**(len(data)-1): data.append(deque(data[-1], base**len(data)))
    now   = time()
    delta = now - prev
    prev  = now
    if delta > pause:
        win = False
        print "Instructions: keep all lines at correct length by hitting Enter %s times/second" % rate
    else:
        clock += delta
        widths = []
        for window in data:
            window.append( delta*rate )
            widths.append( int(0.5+(level*sum(window)/float(len(window)))) )
        win = len(data)>1 and [level]==list(set(widths[:level]))
        print "Level %-3s|" % level, "=v"[win]*level
    print "\n".join("%%9s| %%%ds"%level%(len(window),"#>"[win]*width) for window,width in zip(data[:level], widths))
    raw_input("%-9s| %s "%("%d:%.2d"%((clock-clock%60)/60,clock%60), "^!"[win]*level)) == "q" and exit()
    if win: level+=1

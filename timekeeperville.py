"timekeeperville is a game where you must keep time"
# by Leif Ryge, September 2012, WTFPL
from time import time
from collections import deque
results = []
while True:
    adj   = raw_input("Use default settings? [Yn] ")=="n"
    bpm   = int(adj and raw_input("Initial BPM?        [default=120] ") or 120)
    level = int(adj and raw_input("Initial level?        [default=1] ") or 1  )
    limit = int(adj and raw_input("Initial time limit?  [default=15] ") or 15 )
    base  = int(adj and raw_input("Window size base?     [default=2] ") or 2  )
    pause = int(adj and raw_input("Inactivity threshold? [default=2] ") or 2  )
    accel = int(adj and raw_input("Time to accelerate? [default=180] ") or 180)
    alt   = adj and raw_input("Alternate display mode? [yN] ") == "y" or 0
    data, widths = [deque([1], 1)], [level]
    prev, clock, streak, best, score, clear = 0, 0, 0, 0, 0, "\x1b[H\x1b[2J\x0d"
    while True:
        print clear,
        delta = time()-prev
        prev += delta
        bps   = bpm / 60.0
        if delta > pause:
            win = False
            print "Instructions: hit Enter %s times/minute to keep all rows at the target length" % bpm
        else:
            for window in data: window.append( delta*bps )
            if len(window) == window.maxlen: data.append(deque(window, base**len(data)))
            widths = [ int(level*sum(window)/len(window)+0.5) for window in data[:level] ]
            win    = len(data)>1 and [level]==list(set(widths))
            streak = win and streak+1 or 0
            best   = max(streak, best)
            limit  = (max(0,limit-delta), limit+level+streak )[win]
            clock += delta
            if win and streak < 2 and limit>accel: bpm += 20
            if win and limit: score+=(limit+best)*streak
            print "Level %-3s|%s| %s"%(level, "=!"[win]*level, streak>1 and "%s streak!"%streak or win and ":)" or "%s BPM is %s"%(bpm,('slower','faster')[delta*bps>1]))
        print "\n".join("%%9s|%%%ds| %%s"%(alt and level)%(len(window),".*"[win]*width,len(window)==1 and "%d BPM"%(60/delta) or "") for window,width in zip(data,widths))
        if "q"==raw_input("%-6s%4s%s| Score: %d "%("%2d:%.2d"%(limit/60,limit%60),"[%s]"%best,"=!"[win]*level,score)): break
        if limit == 0: break
        if win: level+=1
    results.append( "%s BPM, %dm %.2ds of play, level %02d, best streak was %s, score %d\n" % (bpm,clock/60,clock%60,level,best,score) )
    while "y"!=raw_input("%s%s\n y to play again, or ctrl-c to quit\n " % (clear, "".join(reversed(results)))): pass

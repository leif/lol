"timekeeperville is a game where you must keep time"
# by Leif Ryge, September 2012, WTFPL
from time import time
from collections import deque
results = []
while True:
    adj   = input("Use default settings?   [Yn] ") == "n"
    bpm   = int(adj and input("Initial BPM?           [120] ") or 120)
    level = int(adj and input("Initial level?           [1] ") or 1  )
    limit = int(adj and input("Initial time limit?     [15] ") or 15 )
    base  = int(adj and input("Window size base?        [2] ") or 2  )
    pause = int(adj and input("Inactivity threshold?    [2] ") or 2  )
    accel = int(adj and input("Time to accelerate?    [180] ") or 180)
    invrt =     adj and input("Invert row length?      [yN] ") == "y"
    alt   =     adj and input("Alternate display mode? [yN] ") == "y" or 0
    prev, clock, streak, best, score, clear, data = 0, 0, 0, 0, 0, "\x1b[H\x1b[2J\x0d", [ deque([1], 1) ]
    while True:
        print(clear, end='')
        delta = time()-prev
        prev += delta
        bps   = bpm/60.0
        if delta > pause:
            print("\nInstructions: hit Enter %s times/minute to keep all rows at the target length."%bpm)
            input("The rows represent your accuracy averaged over increasingly lengthy periods. \n")
            continue
        for window in data: window.append( invrt and 1.0/(delta*bps) or delta*bps )
        if len(window) == base**(len(data)-1): data.append(deque(window, base**len(data)))
        widths = [ int(level*sum(window)/len(window)+0.5) for window in data[:level] ]
        win    = len(data)>1 and [level]==list(set(widths))
        streak = win and streak+1 or 0
        best   = max(streak, best)
        limit  = win and limit+level+streak or max(0, limit-delta)
        clock += delta
        if limit == 0: break
        if win: score+=(limit+best)*streak
        if win and streak<2 and limit>accel: bpm += 20
        print("Level %-3s|%s| %s"%(level, "=!"[win]*level, streak>1 and "%s streak!"%streak or win and ":)" or "%s BPM is %s"%(bpm,('slower','faster')[delta*bps>1])))
        print("\n".join("%%9s|%%%ds| %%s"%((alt or level>29) and level)%(len(window)," *.,-+:;% "[win or 2+((level//4)%8)]*width,len(window)==1 and "%d BPM"%(60//delta) or "<>="[width<level or width==level and 2 or 0]) for window,width in zip(data,widths)))
        if "q"==input("%-6s%4s%s| Score: %d "%("%2d:%.2d"%(limit/60,limit%60),"[%s]"%best,"=!"[win]*level,score)): break
        if win: level+=1
    results.append( "%3s BPM, %dm %.2ds of play, level %02d, best streak was %s, score %d\n" % (bpm,clock/60,clock%60,level,best,score) )
    while "y"!=input("%s%s\n y to play again, or ctrl-c to quit\n " % (clear, "".join(reversed(results)))): pass

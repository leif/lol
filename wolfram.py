"""
Wolfram 1-dimensional cellular automata
"""
__author__  = "Leif Ryge"
__license__ = "WTFPL"

import sys

if len(sys.argv) != 4:
    print "Usage: %s rule width count" % (sys.argv[0],)
    sys.exit(1)
rule, width, count = map(int, sys.argv[1:] )
world = [0] * (width/2) + [ 1 ] + [0] * (width/2)
y = 0
while True:
    print "".join( " *"[cell] for cell in world )
    world = [ rule>>(world[x-1]*4+world[x]*2+world[(x+1)%len(world)])&1
              for x in range(len(world)) ]
    y+=1
    if y >= count:
        break

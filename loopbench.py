#!/usr/bin/env python

def loopbench(f=None):

    import time
    b = 1
    i = 0
    start = time.time()
    d2=0
    while True:
        i+=1
        if f is not None:
            f()
        if i == 2**b:
            d = time.time()-start
            print "%02d:%07.4f %10.2f/sec %3s (%s)" % (d/60,d%60, (i/d), b, i)
            b+=1

if __name__ == "__main__":
    loopbench()

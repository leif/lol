#!/bin/python
"""

This was my solution to a programming excercise which someone told me they once
had to solve during a job interview. I don't recall the details. I belive the
tests passed when it was written in python2, but they no longer do now that
2to3 has been run on it.

>>> list(unrollSpiral( [[ 1, 2 ],
...                     [ 3, 4 ],
...                     [ 5, 6 ]]))
[1, 2, 4, 6, 5, 3]
>>> list(unrollSpiral( [[ 1, 2, 3],
...                     [ 4, 5, 6]]))
[1, 2, 3, 6, 5, 4]
>>> list(unrollSpiral( [[ 1, 2, 3],
...                     [ 4, 5, 6],
...                     [ 7, 8, 9]]))
[1, 2, 3, 6, 9, 8, 7, 4, 5]
>>> list(unrollSpiral( [[ 1,   2,  3,  4],
...                     [ 5,   6,  7,  8],
...                     [ 9,  10, 11, 12],
...                     [ 13, 14, 15, 16]]))
[1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10]
>>> list(unrollSpiral( [[ 1, 2, 3, 4, 5 ]]))
[1, 2, 3, 4, 5]
>>> list(unrollSpiral( [[ 1 ], [ 2 ], [ 3 ], [ 4 ], [ 5 ]]))
[1, 2, 3, 4, 5]
>>> n = 30
>>> for m,r1,r2 in ( map(list,(m,unrollSpiral(m),unrollSpiral_slow(m)))
...     for m in ( [ [ x+(y*w) for x in range(w) ] for y in range(h) ]
...     for w in range(1, n) for h in range(w, n) ) for m in ( m, zip(*m) )):
...         assert r1==r2, (m,r1,r2)
"""

def spiral( w, h ):
    for d in range( (min(w,h)+1)/2 ):
        for x in range( d, w-d ):
            yield x, d
        for y in range( d+1, h-d ):
            yield w-d-1, y
        if d != h-d-1:
            for x in reversed(range( d, w-d-1 )):
                yield x, h-d-1
        if d != w-d-1:
            for y in reversed(range( d+1, h-d-1 )):
                yield d, y

def unrollSpiral( m ):
    for x, y in spiral( len(m[0]), len(m) ): yield m[y][x]

def unrollSpiral_slow( m ):
    "this version takes O(n**2) time and O(n) space instead of O(n) and O(1)"
    while m:
        for i in m[0]: yield i
        m = list(reversed(list(zip(*m[1:]))))

def vis( w, h ):
    from visual import sphere, scene
    scene.autocenter=True
    n = float(w*h)
    for i, (x, y) in enumerate( spiral( w, h ) ):
        sphere( x=x-(w/2.0), y=y-(h/2.0), z=i*0.02, color=(1, 1-(i/n), 0), radius=.5 )

if __name__=="__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "vis":
            vis( *list(map(int, sys.argv[2:])) )
    else:
        import doctest
        print(doctest.testmod())

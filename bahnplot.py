#!/usr/bin/env python

"""
A very simple plotting tool.
"""

__license__ = """
This software may be freely used, modified, and redistributed without any
restrictions except one: you agree to pay the author $1M if you ever tell him
there will be wifi on a long train ride and it turns out that there actually
isn't.
"""

from PIL import Image
import doctest

def scale( v, a, b, A, B ):
    """
    >>> scale( 1, 1, 4, 0, 1, )
    0.0
    >>> scale( 2, 1, 4, 0, 1, )
    0.3333333333333333
    >>> scale( 3, 1, 4, 0, 1, )
    0.6666666666666666
    >>> scale( 4, 1, 4, 0, 1, )
    1.0
    >>> scale( 6, 6, 9, 100, 200 )
    100.0
    >>> scale( 7, 6, 9, 100, 200 )
    133.33333333333331
    >>> scale( 8, 6, 9, 100, 200 )
    166.66666666666666
    >>> scale( 9, 6, 9, 100, 200 )
    200.0
    """
    assert a<=v<=b
    return (float(v-a) / (b-a)) * (B-A) + A

def plot( filename, expr="(1-(1.0/(2**x)))**(2**x)", bounds="0,60,0,1", size="1024x768" ):
    width, height = map(int, size.split("x"))
    minX, maxX, minY, maxY = map(float, bounds.split(','))
    img = Image.new( '1', (width, height) )
    fn = eval("lambda x: %s" % expr)
    for x in range(width):
        X = scale( x, 0, width-1, minX, maxX )
        Y = fn( X )
        try:
            y = int(height-scale( Y, minY, maxY, 1, height ))
        except AssertionError:
            next
        try:
            img.putpixel( (x,y), 1 )
        except:
            print x,y
    img.save( filename )
if __name__ == "__main__":
    from sys import argv
    if len(argv) < 2: 
        print "usage: %s filename [expr [bounds [size]]]" % argv[0]
        doctest.testmod()
    else:
        plot(*argv[1:])

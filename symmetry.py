"""
wat
"""


def trier(f):
 def fn(n):
  try:
   return f(n)
  except:
   return 0
 return fn

dechex=lambda n:int("0x%s"%n,16)
test=lambda n: ((n**2) == trier(int)(hex(dechex(n)**2)[2:].replace('L','')), hex(dechex(n)),hex(dechex(n**2)))
print "\n".join([ "  %s *   %s  =  %s\n%s * %s = %s" % (n,n,n**2,hex(dechex(n)),hex(dechex(n)),hex(dechex(n)**2))  for n in range(100001) if test(n)[0]])


octt=lambda n: oct(n) if n is not 0 else '00'

decbin=lambda n:int("0b%s"%n,2)
decoct=lambda n:int("0%s"%n,8)
testb=lambda n: ((n**2) == trier(int)(bin(trier(decbin)(n)**2)[2:]), bin(trier(decbin)(n)),bin(trier(decbin)(n**2)))
testo=lambda n: ((n**2) == int(octt(trier(decoct)(n)**2)[1:]), octt(trier(decoct)(n)),octt(trier(decoct)(n**2)))

#hexmatches=[ n for n in range(100000) if test(n)[0]]
#binmatches=[ n for n in range(100000) if testb(n)[0]]
#octmatches=[ n for n in range(100000) if testo(n)[0]]


def base(b, n):
    digit = 0
    result = []
    assert b>0
    while b**(digit+1) <= n:
        digit+=1
    while digit>=0:
        value = n / (b**digit)
        if value > 9:
            value = chr(ord('a') + (value - 10))
        result.append(value)
        n%=b**digit
        digit-=1
    return ''.join(map(str,result))

def test_base(b, r=100001):
    results = []
    for i in range(r):
        try:    
            w = int( str(i), b )
            if i**2 == int( base(b, w**2) ):
                results.append(i)
        except:
            continue
    return results

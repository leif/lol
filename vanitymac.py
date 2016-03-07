#!/usr/bin/env python

import sys, re

"""
Note: using vanity MAC addresss is harmful to your anonymity
"""

def string2mac(s):
    "Format a (previously determined to be) suitable string into a MAC"
    w=s.replace(' ','').replace('o','0').replace('i','1').replace('t','7').replace('z','2').replace('s','5')
    r = re.compile('^[a-f0-9]{2,10}$')
    assert r.match(w)
    mac = '0'*(12-len(w))+w
    return ":".join(mac[i*2:(i*2)+2] for i in range(len(mac)/2))

def main(limit=20, wordlist="/usr/share/dict/words"):
    with file(wordlist) as f:
        words = f.read().split()+['foo']
    words = map(str.lower,words)
    r = re.compile('^[a-f0-9oitzs]{2,10}$') # ~687k addresses
    r = re.compile('^[a-f0-9oi]{2,10}$')    # ~32k addresses
    words = filter(r.match, words)
    pairs = [w+' '+w2 for w in words for w2 in words if len(w) + len(w2) <= 10]
#    pairs = [w+w2 for w in words for w2 in words if len(w) + len(w2) <= 10]
#    print len(words),"*",len(pairs),"=",len(words)*len(pairs)
#    tripples = [w+w2 for w in words for w2 in pairs if len(w) + len(w2) <= 10]
    res = words+pairs
    if limit and limit!='0':
        limit=int(limit)
        import random; random.shuffle(res); res=res[:limit]
    return "\n".join("%s %s" % (string2mac(r),r) for r in res)


if __name__ == "__main__":
    print main(*sys.argv[1:])

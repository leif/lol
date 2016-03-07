#!/usr/bin/env python
"""
turnstore.py - repurposing Turn.com's exploitation of Verizon users

This is a client for the free key-value storage service currently provided by
advertising company Turn.com as a side effect of their tracking of Verizon
Wireless users. Turn has said that they intend to disable this service by early
Febrary, 2015.

    UPDATE: They did. This no longer works.

Each HTTP request to Turn.com can store a value on the server via its 'uid'
cookie. If the client also sends something in an 'X-UIDH' header, as all
Verizon Wireless customers currently do, the stored value can be retrieved
later by sending another request containing the same X-UIDH header. The values
in the cookie can be any 63-bit unsigned integer except 0 or 1, and the values
in the X-UIDH header (the keys of our makeshift key value store) can be any
string of 4095 bytes or less.

This program implements a system for using Turn.com to store arbitrary-length
binary files under arbitrary-length keys by splitting the file into 61-bit
chunks (or "words") and hashing the keys.

Artist's statement:

    This is not a useful tool.  Uploading and downloading data this way is very
    slow (although it could be faster if requests were done in parallel) and
    the data could disappear at any time if/when Turn.com changes the way their
    service operates. It is also not very reliable, as occassionally the value
    is not stored and we have not implemented any error correction.

    The contract of the HTTP protocol allows servers to store arbitary data on
    visitors' computers, in the form of cookies. While cookies provide
    essential functionality on the web, most of the cookies on your computer
    are used for tracking you as opposed to doing something helpful.  Users can
    and do choose to clear their cookies periodically in an attempt to unlink
    their web activities, but Turn.com believes that "Clearing cookies is not a
    reliable way for a user to express their desire not to receive tailored
    advertising" so they make every effort to link users' activity even after
    cookies have been cleared.  Due to their desire to track users who have
    cleared their cookies, Turn.com has created a system where a sort of
    "reverse cookie" is set on their server for each request with X-UIDH
    header.

    By repurposing this privacy-hostile technology to provide a novel arbitrary
    storage mechanism, I hope to draw attention to Turn.com's practices and
    also to give people of the internet an opportunity to have some fun with a
    piece of technology that is working against them.  Some might say that
    storing data in these tracking servers is wrong or illegal, while plenty of
    others have already said that what the tracking servers are doing to make
    this possible is already wrong *and* illegal.

    I am releasing this anonymously in case they're litigious assholes about it.

Links:

    http://webpolicy.org/2015/01/14/turn-verizon-zombie-cookie/
    https://www.propublica.org/article/zombie-cookie-the-tracking-cookie-that-you-cant-kill
    http://www.turn.com/blog/in-response-to-propublica
    https://www.turn.com/blog/zombie-cookie-id-to-be-suspended-pending-re-evaluation
    https://www.propublica.org/article/zombie-cookies-slated-to-be-killed
    https://www.propublica.org/article/verizon-will-now-let-users-kill-previously-indestructible-tracking-code


Data format:

    The X-UIDH key we send to Turn.com is 42 bytes of a hash of "$index:$key",
    base64-encoded to resemble a real verizon tracking identifier.  $key is the
    user-provided key, and $index is the word number.

    The second-least-significant bit of each word is always set, to avoid words
    with the forbidden values of zero or one. The least significant bit
    indicates that the data has ended, and the other bits of that final word
    indicate the length of the value in bytes (so that the last word of data
    can be truncated appropriately).  The format is length-suffixed instead of
    length-prefixed so that files can be appended to incrementally. Incremental
    and random-access downloading are not implemented, but could be.


Mitigation:

    Verizon users can avoid Verizon's supercookie by using a VPN, proxy server,
    or Tor.

    Internet users at large can mitigate Turn.com and their ilk's tracking with
    browser extensions like AdBlockPlus and Privacy Badger, and/or by using Tor
    Browser.

    Turn.com could avoid having data be stored on their servers in this manner
    by being decent human beings and not attempting to link users' activity
    before and after they've cleared their cookies. There are also a variety of
    ways that they could continue their tracking and break this script, but I'm
    not going to tell them how except to suggest maybe checking User-Agent? ;)

usage:
 turnstore.py put foo bar        # store the string "bar" under the key "foo"

 cat file | turnstore.py put foo # store a file "file" under the key "foo"

 turnstore.py get foo > file     # retrieve "foo", save as "file"
"""

__copyright__ = "no rights reserved, 2015-01-15"
__license__ = "WTFPL"

import sys, time, hashlib, requests
from itertools import imap, izip, count

url = 'http://ad.turn.com/server/ads.js'

def make_UIDH(key):
    return hashlib.sha256(key).digest()[:42].encode('base64').strip()
    
def put_word(key, value):
    value63 = int(value)
    assert len(key) < 2**12, "key is too big (%s bytes)" % len(key)
    assert 1 < value63 < 2**63, "value %s out of range" % value
    headers = { 'X-UIDH': key }
    cookies = { 'uid': str(value63) }
    r = requests.get(url, cookies=cookies, headers=headers)

def get_word(key):
    headers = { 'X-UIDH': key }
    r = requests.get(url, headers=headers)
    return int(r.cookies['uid'])

def changeWordSize (words, inSize, outSize):
    """
    >>> list( changeWordSize( [255, 18], 8, 1 ) )
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0]
    >>> list( changeWordSize( [255, 18], 8, 4 ) )
    [15, 15, 1, 2]
    >>> list( changeWordSize( [15, 15, 1, 2], 4, 8 ) )
    [255, 18]

    NOTE: this will sometimes add trailing null words when inSize is not a
    factor or multiple of outSize:
    >>> list( changeWordSize( [255, 18], 8, 5 ) )
    [31, 28, 9, 0]
    
    This function was borrowed from github.com/leif/bananaphone
    """
    assert inSize  > 0
    assert outSize > 0
    bits  = 0
    value = 0
    for word in words:
        assert type(word) in (int, long), "words must be int or long, got %s" % type(word)
        assert 0 <= word < 2 ** inSize  , "words must be in range 0 to 2**%s-1, got %s" % (inSize, word)
        value  = value << inSize
        value += word
        bits  += inSize
        while outSize <= bits:
            bits    -= outSize
            newWord  = value >> bits
            value   -= newWord << bits
            yield newWord
    if bits:
        yield value << (outSize - bits)

def put(key, data=None):
    if data is None:
        data = iter(lambda: sys.stdin.read(1), "")
        bit_length = "?"
        word_count = "?"
    else:
        bit_length = len(data) * 8
        word_count = (bit_length / 61) + bool(bit_length % 61)
    counter = count()
    words = changeWordSize(imap(ord, (d for d,i in izip(data, counter))), 8, 61)
    print "%s bits will be %s 61-bit words." % (bit_length, word_count,)
    startTime = time.time()
    for i, word in enumerate(words):
        word<<=2
        word|=2 # always set 2nd bit to avoid zero or one values
        bps = int((i * 61.0) / (time.time() - startTime))
        hashkey = make_UIDH("%s:%s" % (i, key))
        print "Storing word %s of %s, %s = %s, %s bps" % (i, word_count, hashkey, word, bps)
        put_word(hashkey, word)
    hashkey = make_UIDH("%s:%s" % (i+1, key))
    byte_length = counter.next()
    encoded_length = (byte_length << 1) | 1
    print "storing trailer %s = %s (%s bytes)" % (hashkey, encoded_length, byte_length)
    put_word(hashkey, encoded_length)
    return "Wrote %s bytes in %s cookies." % (byte_length, i+2)

def get(key):
    i = 0
    words = []
    while True:
        hashkey = make_UIDH("%s:%s" % (i, key))
        word = get_word(hashkey)
        if word & 1:
            length = word >> 1
            break
        else:
            realword = word >> 2
            words.append(realword)
            i+=1
    data = "".join(map(chr,changeWordSize(words, 61, 8)))
    assert len(data) >= length, "impossible length %s (have %s words, %s bytes, last word was %s: %s = %s)" % (length, len(words), len(data), i, hashkey, word)
    return data[:length]

if __name__ == "__main__":
    try:
        f=globals()[sys.argv[1]]
    except (IndexError, KeyError):
        print __doc__
    else:
        sys.stdout.write(f(*sys.argv[2:]))

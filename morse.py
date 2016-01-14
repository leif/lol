"""
dedicated to the person who was sending me morse coded twitter DMs for a while.

this seems to mostly work though it did fail to decode a few of their messages.
"""

A2M  = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
        
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.',  ' ': '/' 
        }

M2A = dict((v,k) for k,v in A2M.items())

encode = lambda s: "".join(A2M.get(c.upper(), c)+' ' for c in s)
decode = lambda s: "".join(M2A.get(c, c) for c in s.split())

if __name__ == '__main__':
    import sys
    print globals()[sys.argv[1]](sys.argv[2])

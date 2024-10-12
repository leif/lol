from random import randint

# https://en.wikipedia.org/wiki/Irwin%E2%80%93Hall_distribution

def test(r, n, s):
    res = {}
    for i in range(n):
        v = sum(randint(0, r // s) for j in range(s))
        if v in res:
            res[v] += 1
        else:
            res[v] = 1
    for i in range(r):
        print(f"{s:>2} samples {n} iterations: result {i}: {'*'*int((res[i]/(n/r))*30)} {res[i]}")

test(20, 100000, 1)
test(20, 100000, 2)
test(20, 100000, 4)
test(20, 100000, 5)
test(20, 400000, 10)

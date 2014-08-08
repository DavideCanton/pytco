__author__ = 'Kami'

from pytco import tco
from timeit import default_timer as timer
import sys


@tco
def f(l, acc=0, i=0):
    if i == len(l):
        return acc
    return f(l, acc + l[i], i + 1)


def g(l, acc=0, i=0):
    if i == len(l):
        return acc
    return g(l, acc + l[i], i + 1)


@tco
def f2(n, acc=1):
    if n <= 1:
        return acc
    return f2(n - 1, acc * n)


def g2(n, acc=1):
    if n <= 1:
        return acc
    return g2(n - 1, acc * n)


if __name__ == "__main__":
    sys.setrecursionlimit(2000)

    arg = [2, 6, 7, 3, 1, 2, 5, 6]

    start = timer()
    r1 = f(arg)
    end1 = timer() - start

    print("With TCO:", end1)

    start = timer()
    r2 = g(arg)
    end2 = timer() - start

    print("Without TCO:", end2)

    # print(r1, r2)
    print(r1 == r2)
    print("Time ratio:", end2 / end1)
__author__ = 'Kami'

from pytco import tco
from timeit import default_timer as timer
import sys


@tco
def f(n, acc=1):
    if n <= 1:
        return acc
    return f(n - 1, acc * n)


def g(n, acc=1):
    if n <= 1:
        return acc
    return g(n - 1, acc * n)


if __name__ == "__main__":
    sys.setrecursionlimit(2000)

    start = timer()
    r1 = f(1000)
    end = timer() - start

    print("With TCO:", end)

    start = timer()
    r2 = g(1000)
    end = timer() - start

    print("Without TCO:", end)

    print(r1 == r2)
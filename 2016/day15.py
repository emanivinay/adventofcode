import sys
from math import lcm


def main():
    discs = [line.split() for line in sys.stdin.readlines()]
    discs = [(int(disc[3]), int(disc[-1][:-1])) for disc in discs]

    # 0. Each disc i can be represented as disc i = (Ai, Bi) where Ai is the # of slots and Bi is its slot at t=0
    # 1. For starting time t and disc i, we have (Bi + t + i + 1) % Ai = 0 => t % Ai = (Ai - Di % Ai) % Ai = Ci
    #    where Di = Bi + i + 1
    #      and Ci = (Ai - Di % Ai) % Ai
    # 2. Starting t must satisfy t % Ai = Ci for all discs i
    # 3. In general, if L is the lcm of all Ai, then valid starting t will repeat with a frequency of L.
    # 4. i.e., if t0 is the first valid starting t, then every t0 + j * L will be a valid starting point.
    # 5. Extended Euclidean algorithm can be used to efficiently compute t0.
    for t in range(10000000):
        if all((b + t + i + 1) % a == 0 for i, (a, b) in enumerate(discs)):
            print(t)
            break


main()
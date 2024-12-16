import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    weights = [int(l) for l in sys.stdin.read().split('\n')]
    N = len(weights)
    S = sum(weights)
    need = S // 3
    need2 = S // 4

    dp = [[(N + 1, 1)] * (need + 1) for _ in range(need + 1)]
    dp[0][0] = (0, 1)

    dp2 = [[[(N + 1, 1)] * (need2 + 1) for _ in range(need2 + 1)] for _ in range(need2 + 1)]
    dp2[0][0][0] = (0, 1)

    total = 0
    for w in weights:
        print(w)
        for f in range(need, -1, -1):
            for s in range(need, -1, -1):
                t = total - f - s
                if t < 0 or t > need:
                    continue
                mn, pd = dp[f][s]
                if f + w <= need:
                    dp[f + w][s] = min(dp[f + w][s], (mn + 1, pd * w))
                if s + w <= need:
                    dp[f][s + w] = min(dp[f][s + w], (mn, pd))
        
        for f2 in range(need2, -1, -1):
            for s2 in range(need2, -1, -1):
                for t2 in range(min(need2, total - f2 - s2), max(-1, total - f2- s2 - need2 -1), -1):
                    r2 = total - f2 - s2 - t2
                    # t2 <= total - f2 - s2
                    # t2 > total - f2 - s2 - need2 - 1
                    if r2 < 0 or r2 > need2:
                        continue
                    mn, pd = dp2[f2][s2][t2]
                    if f2 + w <= need2:
                        dp2[f2 + w][s2][t2] = min(dp2[f2 + w][s2][t2], (mn + 1, pd * w))
                    if s2 + w <= need2:
                        dp2[f2][s2 + w][t2] = min(dp2[f2][s2 + w][t2], (mn, pd))
                    if t2 + w <= need2:
                        dp2[f2][s2][t2 + w] = min(dp2[f2][s2][t2 + w], (mn, pd))
        
        total += w

    # Part 1 took ~1s and Part 2 about ~2m35s on my M1 Mac.
    print(dp[need][need])
    print(dp2[need2][need2][need2])


if __name__ == '__main__':
    main()

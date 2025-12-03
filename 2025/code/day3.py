import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def max_power(bank, K):
    N = len(bank)
    BIG = 1 << 80
    @functools.lru_cache(maxsize=None)
    def f(i, k):
        if k == 0:
            return 0
        if i == N:
            return -BIG
        ret = f(i + 1, k)
        ret = max(ret, (10 ** (k - 1)) * bank[i] + f(i + 1, k - 1))
        return ret

    return f(0, K)


def main():
    input_lines = sys.stdin.read().split('\n')
    part1, part2 = 0, 0
    for line in input_lines:
        bank = [int(d) for d in line]
        part1 += max_power(bank, 2)
        part2 += max_power(bank, 12)

    print(part1, part2)


if __name__ == '__main__':
    main()

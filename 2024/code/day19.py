import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def is_possible(design, patterns_by_first_char):
    N = len(design)
    dp = [0] * (N + 1)
    dp[N] = 1
    for i in range(N - 1, -1, -1):
        for pat in patterns_by_first_char[design[i]]:
            if len(pat) <= N - i and pat == design[i : i + len(pat)]:
                dp[i] += dp[i + len(pat)]
    return dp[0]


def main():
    input_lines = sys.stdin.read().split('\n')
    patterns_by_first_char = collections.defaultdict(list)
    for pat in input_lines[0].split(', '):
        patterns_by_first_char[pat[0]].append(pat)

    part1, part2 = 0, 0
    for design in input_lines[2:]:
        temp = is_possible(design, patterns_by_first_char)
        part1 += temp > 0
        part2 += temp

    print(part1, part2)


if __name__ == '__main__':
    main()

import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def is_number_valid(num):
    s = str(num)
    N = len(s)
    if N % 2 == 1:
        return True
    d = N // 2
    return s[:d] != s[d:]


def main():
    input_lines = sys.stdin.read().split('\n')
    ranges = input_lines[0].split(',')
    invalid_set = set()
    for arange in ranges:
        start, end = arange.split('-')
        start, end = int(start), int(end)
        for x in range(start, end + 1):
            if not is_number_valid(x):
                invalid_set.add(x)

    print(sum(invalid_set), min(invalid_set), max(invalid_set))


if __name__ == '__main__':
    main()

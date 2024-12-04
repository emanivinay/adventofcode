import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    input_lines = sys.stdin.read().split('\n')
    pairs = [split_ints(line) for line in input_lines]
    left = sorted(pair[0] for pair in pairs)
    right = sorted(pair[1] for pair in pairs)
    result1 = sum(abs(l - r) for l, r in zip(left, right))
    print(result1)

    right_counter = collections.Counter(right)
    result2 = sum(l * right_counter[l] for l in left)
    print(result2)


if __name__ == '__main__':
    main()

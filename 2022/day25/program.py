import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


SNAFU_DIGITS = {
    '0': 0,
    '1': 1,
    '2': 2,
    '-': -1,
    '=': -2,
}

def snafu_value(s):
    ret = 0
    for i, c in enumerate(s[::-1]):
        ret += (5 ** i) * SNAFU_DIGITS[c]
    return ret


def to_snafu(number):
    if number == 0:
        return ''
    
    rem = number % 5
    for d, r in SNAFU_DIGITS.items():
        if (r + 5) % 5 == rem:
            pref = (number - r) // 5
            return to_snafu(pref) + d
    return ''


def main():
    input_lines = sys.stdin.read().split('\n')
    # part 1
    total = sum(snafu_value(line.strip()) for line in input_lines)
    print(to_snafu(total))


if __name__ == '__main__':
    main()
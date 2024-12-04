import sys
import collections
import itertools
import functools
import re


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


DIGIT_WORD_MAP = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

def extract_possibly_worded_digits(s: str):
    i, N = 0, len(s)
    ret = []
    while i < N:
        if s[i].isdigit():
            ret.append(int(s[i]))
            i += 1
        else:
            for word, value in DIGIT_WORD_MAP.items():
                if s[i:].startswith(word):
                    ret.append(value)
                    i += 1
                    break
            else:
                i += 1
    return ret


def main():
    input_lines = sys.stdin.read().split('\n')
    # parts 1 and 2
    total, total2 = 0, 0
    for line in input_lines:
        digits = re.findall('[0-9]', line)
        if digits:
            total += int(digits[0]) * 10 + int(digits[-1])

        digits2 = extract_possibly_worded_digits(line)
        if digits2:
            line_value = digits2[0] * 10 + digits2[-1]
            total2 += line_value

    print(total, total2)

if __name__ == '__main__':
    main()
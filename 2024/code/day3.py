import sys
import collections
import itertools
import functools
import re


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    code = sys.stdin.read().strip()

    part1, part2, enabled = 0, 0, True
    for match in re.finditer(r"mul\([0-9]{1,3}\,[0-9]{1,3}\)|do\(\)|don't\(\)", code):
        matched = match.group(0)
        if matched == "do()":
            enabled = True
        elif matched == "don't()":
            enabled = False
        else:
            x, y = [int(w) for w in matched[4:-1].split(",")]
            part1 += x * y
            if enabled:
                part2 += x * y
    print(part1, part2)


if __name__ == '__main__':
    main()
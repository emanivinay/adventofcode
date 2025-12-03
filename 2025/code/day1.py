import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    input_lines = sys.stdin.read().split('\n')
    dial = 50
    part1, part2 = 0, 0
    for line in input_lines:
        dir, amount = line[0], int(line[1:])
        delta = 1 if dir == 'R' else -1
        for _ in range(amount):
            dial += delta
            if dial < 0:
                dial += 100
            elif dial >= 100:
                dial -= 100
            if dial == 0:
                part2 += 1
        
        part1 += dial == 0

    print(part1, part2)


if __name__ == '__main__':
    main()
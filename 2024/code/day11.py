import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


@functools.lru_cache(maxsize=None)
def xform_stone(stone, steps):
    if steps == 0:
        return 1
    if stone == 0:
        return xform_stone(1, steps - 1)
    s = str(stone)
    if len(s) % 2 == 0:
        l, r = s[:len(s) // 2], s[len(s) // 2:]
        return xform_stone(int(l), steps - 1) + xform_stone(int(r), steps - 1)
    return xform_stone(2024 * stone, steps - 1)


def main():
    stones = [int(w) for w in sys.stdin.read().split('\n')[0].split()]
    print(sum(xform_stone(stone, 25) for stone in stones))
    print(sum(xform_stone(stone, 75) for stone in stones))


if __name__ == '__main__':
    main()


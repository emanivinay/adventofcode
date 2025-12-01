import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def re_head_at_0(circle):
    i = circle.index(0)
    return circle[i:] + circle[:i]


def simulate(elfs, marbles):
    circle = [0]
    elf_scores = [0] * elfs
    for i in range(1, marbles):
        if i % 23 == 0:
            elf_scores[i % elfs] += i + circle[-7]
            circle = circle[-6:] + circle[:-7]
        elif len(circle) < 3:
            circle = [i, *circle]
        else:
            circle.insert(2, i)
            circle = circle[2:] + circle[:2]
    return circle, elf_scores


def main():
    # 491 elfs, 71059 marbles
    circle, elf_scores = simulate(491, 47)
    print(max(elf_scores))


if __name__ == '__main__':
    main()

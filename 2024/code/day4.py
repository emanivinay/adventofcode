import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def sequence_pattern_counter(pattern):
    P = len(pattern)
    tail = ""

    def reset():
        nonlocal tail
        tail = ""
    
    def counter(seq):
        nonlocal tail
        ret = 0
        for c in seq:
            tail += c
            tail = tail[-P:]
            if tail == pattern:
                ret += 1
        return ret

    return counter, reset


def count_word_in_grid(grid, word):
    H, W = len(grid), len(grid[0])
    counter, reset = sequence_pattern_counter(word)
    ret = 0
    for i in range(H):
        reset()
        ret += counter(grid[i])
    
    for j in range(W):
        reset()
        ret += counter(grid[i][j] for i in range(H))
    
    for d in range(H + W - 1):
        # i + j = d, 0 <= i < H, 0 <= d - i < W
        # i <= d, i >= 0, i < H, i >= d - W + 1
        # i >= max(0, d - W + 1), i < min(d + 1, H)
        reset()
        ret += counter(grid[i][d - i] for i in range(max(0, d - W + 1), min(d + 1, H)))
    
    for d in range(H - 1, -W, -1):
        # i - j = d, 0 <= i < H, 0 <= i - d < W
        # i >= d, 0, i < min(H, W + d)
        reset()
        ret += counter(grid[i][i - d] for i in range(max(d, 0), min(d + W, H)))

    return ret


def main():
    grid = sys.stdin.read().split('\n')
    part1 = count_word_in_grid(grid, "XMAS") + count_word_in_grid(grid, "SAMX")
    print(part1)

    H, W = len(grid), len(grid[0])
    part2 = 0
    SM_PAIRS = ("SM", "MS")
    for i in range(1, H - 1):
        for j in range(1, W - 1):
            if grid[i][j] == 'A':
                l1, l2 = grid[i - 1][j - 1], grid[i + 1][j + 1]
                l3, l4 = grid[i - 1][j + 1], grid[i + 1][j - 1]
                if l1 + l2 in SM_PAIRS and l3 + l4 in SM_PAIRS:
                    part2 += 1
    print(part2)


if __name__ == '__main__':
    main()
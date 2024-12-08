import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    grid = sys.stdin.read().split('\n')
    H, W = len(grid), len(grid[0])

    def is_inside_grid(y, x):
        return 0 <= y < H and 0 <= x < W

    def gen_antinodes(y1, x1, y2, x2):
        y3, x3 = 2 * y2 - y1, 2 * x2 - x1
        y4, x4 = 2 * y1 - y2, 2 * x1 - x2
        if is_inside_grid(y3, x3):
            yield (y3, x3)
        if is_inside_grid(y4, x4):
            yield (y4, x4)

    def gen_antinodes_part2(y1, x1, y2, x2):
        dy, dx = y2 - y1, x2 - x1
        for t in range(-50, 51):
            y, x = y1 + t * dy, x1 + t * dx
            if is_inside_grid(y, x):
                yield (y, x)

    antennas_by_freq = collections.defaultdict(list)
    for h in range(H):
        for w in range(W):
            if grid[h][w] != '.':
                antennas_by_freq[grid[h][w]].append((h, w))

    antinode_set = set()
    antinode_set_part2 = set()
    for antennas in antennas_by_freq.values():
        M = len(antennas)
        for i in range(M):
            for j in range(i):
                for y, x in gen_antinodes(*antennas[i], *antennas[j]):
                    antinode_set.add((y, x))
                for y, x in gen_antinodes_part2(*antennas[i], *antennas[j]):
                    antinode_set_part2.add((y, x))

    print(len(antinode_set), len(antinode_set_part2))


if __name__ == '__main__':
    main()
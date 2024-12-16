import sys
import collections
import itertools
import functools
import re


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)

H, W = 103, 101


def modulo(x, N):
    if x >= 0:
        return x % N
    return (N - (-x) % N) % N


def check_row(row, i, l):
    return set(row[i: i + l]) == {'*'}


def grid_after_t_sec(robots, t):
    grid = [[' '] * W for _ in range(H)]
    for x, y, vx, vy in robots:
        x2 = modulo(x + vx * t, W)
        y2 = modulo(y + vy * t, H)
        grid[y2][x2] = '*'
    
    for h in range(H):
        for w in range(W):
            if w >= 2 and w + 2 < W and h + 2 < H:
                if check_row(grid[h], w, 1) and check_row(grid[h + 1], w - 1, 3) and check_row(grid[h + 2], w - 2, 5):
                    return [''.join(row) for row in grid], True

    return [''.join(row) for row in grid], False


def main():
    robots = []
    for _ in range(500):
        line = sys.stdin.readline()
        _, x, y, _, vx, vy = re.split(r'[=, ]', line)
        x, y, vx, vy = [int(w) for w in [x, y, vx, vy]]
        robots.append((x, y, vx, vy))

    counts = [[0] * W for _ in range(H)]
    quads = [[0, 0], [0, 0]]
    for x, y, vx, vy in robots:
        x2 = modulo(x + vx * 100, W)
        y2 = modulo(y + vy * 100, H)
        counts[y2][x2] += 1
        if y2 == H // 2 or x2 == W // 2:
            continue
        quads[y2 >= (H + 1) // 2][x2 >= (W + 1) // 2] += 1

    
    part1 = quads[0][0] * quads[0][1] * quads[1][0] * quads[1][1]
    print(part1)

    # Simulate robot movement upto ~10K seconds to figure out probable 
    # christmas tree formation times.
    grid, _ = grid_after_t_sec(robots, 7051)
    for row in grid:
        print(row)


if __name__ == '__main__':
    main()

import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


def gen_points_between(a, b):
    if a <= b:
        yield from range(a, b + 1)
    yield from range(a, b - 1, -1)


def gen_path_between(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    if x1 == x2:
        yield from ((x1, y) for y in gen_points_between(y1, y2))
    else:
        yield from ((x, y1) for x in gen_points_between(x1, x2))


split_ints = lambda line: split_line_to_type(line, int)

NMAX = 1024

def paint_rock_line(line, grid):
    points = line.split(' -> ')
    points = [[int(w) for w in pt.split(',')] for pt in points]
    N = len(points)
    y_max = 0
    for i in range(1, N):
        for x, y in gen_path_between(points[i - 1], points[i]):
            grid[y][x] = '#'
            y_max = max(y, y_max)
    
    return y_max


def simulate_fall(grid):
    x, y = 500, 0
    while y < NMAX - 1:
        below = grid[y + 1][x]
        if below == '_':
            y += 1
        elif x == 0:
            return False
        elif x >= 1 and grid[y + 1][x - 1] == '_':
            y, x = y + 1, x - 1
        elif x + 1 == NMAX:
            return False
        elif x + 1 < NMAX and grid[y + 1][x + 1] == '_':
            y, x = y + 1, x + 1
        else:
            grid[y][x] = '.'
            return True

    return False


def simulate_fall2(grid, h_max):
    x, y = 500, 0
    while y < h_max:
        if grid[y + 1][x] == '_':
            y = y + 1
        elif grid[y + 1][x - 1] == '_':
            y, x = y + 1, x - 1
        elif grid[y + 1][x + 1] == '_':
            y, x = y + 1, x + 1
        else:
            grid[y][x] = '.'
            return


def main():
    input_lines = sys.stdin.read().split('\n')
    grid = [['_'] * NMAX for _ in range(NMAX)]
    h_max = 0
    for line in input_lines:
        h_max = max(h_max, paint_rock_line(line, grid))
    
    # part 1
    settled = 0
    while simulate_fall(grid):
        settled += 1
    print(settled)

    # part 2
    grid2 = [['_'] * NMAX for _ in range(NMAX)]
    for line in input_lines:
        paint_rock_line(line, grid2)
    for x in range(NMAX):
        grid2[h_max + 2][x] = '#'

    settled = 0
    while grid2[0][500] == '_':
        settled += 1
        simulate_fall2(grid2, h_max + 2)
    
    print(settled)


if __name__ == '__main__':
    main()
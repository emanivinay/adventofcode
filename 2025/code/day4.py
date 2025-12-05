import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def gen_removable_rolls(grid):
    H, W = len(grid), len(grid[0])

    for i in range(H):
        for j in range(W):
            if grid[i][j] == '@':
                rolls_adj = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dy == 0 and dx == 0:
                            continue
                        if i + dy < 0 or i + dy >= H or j + dx < 0 or j + dx >= W:
                            continue
                        rolls_adj += grid[i + dy][j + dx] == '@'
                if rolls_adj < 4:
                    yield (i, j)


def remove_all_removable_rolls(grid):
    H, W = len(grid), len(grid[0])
    removable = set(gen_removable_rolls(grid))
    new_grid = []
    for i in range(H):
        row = []
        for j in range(W):
            if (i, j) in removable or grid[i][j] != '@':
                row.append('.')
            else:
                row.append('@')
        new_grid.append(''.join(row))
    return new_grid, len(removable)


def main():
    grid = sys.stdin.read().split('\n')
    # part 1
    print(len(list(gen_removable_rolls(grid))))

    # part 2
    part2 = 0
    while True:
        new_grid, removed = remove_all_removable_rolls(grid)
        if not removed:
            break
        grid = new_grid
        part2 += removed
    
    print(part2)


if __name__ == '__main__':
    main()

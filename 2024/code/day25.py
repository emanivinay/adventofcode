import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    grids = sys.stdin.read().split('\n\n')
    grids = [grid.split('\n') for grid in grids]

    def column_heights(grid):
        columns = [0] * W
        for i in range(W):
            for j in range(1, H):
                columns[i] += grid[j][i] == '#'
        return columns

    def do_lock_key_fit_together(key, lock):
        return all(key[col] + lock[col] <= 5 for col in range(W))

    H, W = 7, 5
    keys, locks = [], []
    for grid in grids:
        if grid[0] == '#' * W:
            locks.append(column_heights(grid))
        else:
            keys.append(column_heights(grid[::-1]))

    part1 = 0
    for key in keys:
        for lock in locks:
            if do_lock_key_fit_together(key, lock):
                part1 += 1
    print(part1)
    

if __name__ == '__main__':
    main()

import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)

DIRECTIONS = {
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
    'v': (1, 0)
}

def print_grid(grid):
    for row in grid:
        print(*row, sep='')
    print()


def can_move_vertically_in_dir_part2(grid, y, x, dir):
    dy, _ = DIRECTIONS[dir]
    y2 = y + dy
    if grid[y][x] == '@':
        return grid[y2][x] != '#'

    x0 = x
    x1 = x0 + 1
    return grid[y2][x0] != '#' and grid[y2][x1] != '#'


def gen_touching_boxes_in_dir_part2(grid, y, x, dir):
    dy, dx = DIRECTIONS[dir]
    y2 = y + dy
    x0 = x
    x1 = x0 + 1
    if grid[y2][x0] == ']':
        yield (y2, x0 - 1)
    elif grid[y2][x0] == '[':
        yield (y2, x0)
    if grid[y2][x1] == '[':
        yield (y2, x1)


def simulate_robot_movement_part2(grid, y, x, dir):
    dy, dx = DIRECTIONS[dir]
    if dy == 0:
        return simulate_robot_movement(grid, y, x, dir)

    y2, x2 = y + dy, x + dx
    moving = set()

    if grid[y2][x2] == '[':
        moving.add((y2, x2))
    elif grid[y2][x2] == ']':
        moving.add((y2, x2 - 1))

    while moving and all(can_move_vertically_in_dir_part2(grid, *box, dir) for box in moving):
        moving2 = set()
        for box in moving:
            for next_box in gen_touching_boxes_in_dir_part2(grid, *box, dir):
                if next_box in moving:
                    continue
                moving2.add(next_box)
        if not moving2:
            break
        moving |= moving2
    
    moving.add((y, x))
    if y == 3 and x == 13 and dy == 1:
        print(moving)

    if all(can_move_vertically_in_dir_part2(grid, *box, dir) for box in moving):
        # move all these boxes vertically.
        for (y_, x_) in sorted(moving, key=lambda b: (-dy * b[0], b[1])):
            if (y_, x_) == (y, x):
                continue
            y2 = y_ + dy
            x0 = x_ if grid[y_][x_] == '[' else (x_ - 1)
            x1 = x0 + 1
            grid[y2][x0] = '['
            grid[y2][x1] = ']'
            grid[y_][x0] = grid[y_][x1] = '.'
        
        grid[y + dy][x] = '@'
        grid[y][x] = '.'
        return (y + dy, x)
    else:
        return (y, x)


def simulate_robot_movement(grid, y, x, dir):
    dy, dx = DIRECTIONS[dir]
    y2, x2 = y, x
    train = []
    while grid[y2][x2] in '@O[]':
        train.append(grid[y2][x2])
        y2, x2 = y2 + dy, x2 + dx
    # train is (x, y) -> (x2, y2)
    train = train[::-1]
    if grid[y2][x2] == '#':
        return y, x

    for i, c in enumerate(train):
        y3, x3 = y2 - i * dy, x2 - i * dx
        grid[y3][x3] = c
    grid[y][x] = '.'

    return y + dy, x + dx


def main():
    grid = []
    program = []
    for line in sys.stdin.read().split('\n'):
        if not line:
            continue
        if '#' in line:
            grid.append(list(line))
        else:
            program.append(line)
    
    program = ''.join(program)
    H, W = len(grid), len(grid[0])

    ry, rx = -1, -1
    for y in range(H):
        for x in range(W):
            if grid[y][x] == '@':
                ry, rx = y, x

    def widen(cell):
        return {
            '@': '@.',
            'O': '[]',
            '#': '##',
            '.': '..',
        }[cell]

    grid2 = [''.join(widen(cell) for cell in row) for row in grid]
    grid2 = [list(row) for row in grid2]

    print_grid(grid2)
    ry2, rx2 = ry, rx * 2
    for d in program:
        # print()
        # print(*DIRECTIONS[d])
        ry2, rx2 = simulate_robot_movement_part2(grid2, ry2, rx2, d)
        # print_grid(grid2)
        ry, rx = simulate_robot_movement(grid, ry, rx, d)

    part1, part2 = 0, 0
    for y in range(H):
        for x in range(W):
            if grid[y][x] == 'O':
                part1 += 100 * y + x
        for x in range(2 * W):
            if grid2[y][x] == '[':
                part2 += 100 * y + x

    print(part1, part2)


if __name__ == '__main__':
    main()

import sys

question_part = 1

def is_corner_cell(y, x, n_dim):
    if question_part == 1:
        return False
    return (y, x) in [(0, 0), (0, n_dim - 1), (n_dim - 1, 0), (n_dim - 1, n_dim - 1)]


def gen_lit_neighbors(grid, y, x, n_dim):
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dy == 0 and dx == 0:
                continue
            yy, xx = y + dy, x + dx
            if 0 <= min(yy, xx) <= max(yy, xx) < n_dim and (grid[yy][xx] == '#' or is_corner_cell(yy, xx, n_dim)):
                yield 1


def single_step_update(grid):
    n_dim = len(grid)
    grid2 = [['.'] * n_dim for _ in range(n_dim)]
    for i in range(n_dim):
        for j in range(n_dim):
            neighbors_on = sum(gen_lit_neighbors(grid, i, j, n_dim))
            if grid[i][j] == '#' and neighbors_on in (2, 3):
                grid2[i][j] = '#'
            elif grid[i][j] == '.' and neighbors_on == 3:
                grid2[i][j] = '#'
    
    return grid2


def main():
    grid = [list(line.strip()) for line in sys.stdin.readlines()]
    grid2 = [row[:] for row in grid]
    n_dim = len(grid)
    # part1
    for _ in range(100):
        grid = single_step_update(grid)
    
    num_lights_on = sum(row.count('#') for row in grid)
    print(num_lights_on)

    global question_part
    question_part = 2

    for _ in range(100):
        grid2 = single_step_update(grid2)
    num_lights_on = 0
    for y in range(n_dim):
        for x in range(n_dim):
            if grid2[y][x] == '#' or is_corner_cell(y, x, n_dim):
                num_lights_on += 1
    print(num_lights_on)


main()
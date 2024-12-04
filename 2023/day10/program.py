import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3
MOVE_BY_DIR = [(-1, 0), (0, 1), (1, 0), (0, -1)]

PIPE_TYPES = {
    '|': [0, 2],
    '-': [1, 3],
    'L': [0, 1],
    'J': [0, 3],
    '7': [2, 3],
    'F': [1, 2],
    '.': [],
}

def get_horizontal_sections(pipe):
    if pipe == '-':
        return ['a', 'b']
    elif pipe == 'L' or pipe == 'F':
        return ['b']
    elif pipe == 'J' or pipe == '7':
        return ['a']
    return []

def get_opposite_dir(direction):
    return direction ^ 2


def move_in_dir(y, x, entry_dir, grid):
    pipe = PIPE_TYPES.get(grid[y][x], [])
    for edir in pipe:
        if edir != entry_dir:
            dy, dx = MOVE_BY_DIR[edir]
            return y + dy, x + dx, get_opposite_dir(edir)
    return 0, 0, 4


def main():
    input_lines = sys.stdin.read().split('\n')
    grid = [list(line.strip()) for line in input_lines]
    R = len(grid)
    C = len(grid[0])
    print(R, C)

    start = 0, 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                start = r, c
                entries = []
                for d in [NORTH, EAST, SOUTH, WEST]:
                    dy, dx = MOVE_BY_DIR[d]
                    y2, x2 = r + dy, c + dx
                    if y2 < 0 or y2 >= R or x2 < 0 or x2 >= C:
                        continue
                    o = get_opposite_dir(d)
                    if o in PIPE_TYPES[grid[y2][x2]]:
                        entries.append(d)
                
                entries.sort()
                for sign, ents in PIPE_TYPES.items():
                    if ents == entries:
                        grid[r][c] = sign
    
    y, x, entry_dir, i = *start, SOUTH, 0

    animal = []
    covered = collections.defaultdict(list)
    while i == 0 or ((y, x) != start):
        if grid[y][x] == '-':
            covered[x].append(y)
        i += 1
        animal.append((y, x))
        y, x, entry_dir = move_in_dir(y, x, entry_dir, grid)
    
    print(i // 2)

    crossings = collections.defaultdict(list)
    for y, x in animal:
        pipe = grid[y][x]
        sections = get_horizontal_sections(pipe)
        for section in sections:
            crossings[x].append((y, section))

    ret = 0
    for x, vertical in crossings.items():
        vertical.sort()
    
    print(ret)


if __name__ == '__main__':
    main()
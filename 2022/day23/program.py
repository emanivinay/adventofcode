import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


# N, S, W, E = (x, y) coordinates
CARDINAL_DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# NW, NE, SW, SE
DIAGONAL_DIRECTIONS = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

ALL_DIRECTIONS = CARDINAL_DIRECTIONS + DIAGONAL_DIRECTIONS

DIRECTION_CHECK_MAP = {
    0: [0, 4, 5],
    1: [1, 6, 7],
    2: [2, 4, 6],
    3: [3, 5, 7],
}

def simulate_round(elves, order):
    proposed_sites = collections.defaultdict(list)
    elf_positions = set(elves)

    non_proposing = []
    for x, y in elves:
        site = None
        if all((x + dx, y + dy) not in elf_positions for dx, dy in ALL_DIRECTIONS):
            non_proposing.append((x, y))
            continue
        for i in range(4):
            dir = (i + order) % 4
            px, py = ALL_DIRECTIONS[dir]
            dirs_to_check = [ALL_DIRECTIONS[x] for x in DIRECTION_CHECK_MAP[dir]]
            if all((x + dx, y + dy) not in elf_positions for dx, dy in dirs_to_check):
                site = x + px, y + py
                break
        
        if site is not None:
            proposed_sites[site].append((x, y))
        else:
            non_proposing.append((x, y))
    
    moved = False
    new_elf_positions = []
    for new_site, elves in proposed_sites.items():
        if len(elves) == 1:
            new_elf_positions.append(new_site)
            moved = True
        else:
            for elf in elves:
                new_elf_positions.append(elf)
    
    new_elf_positions += non_proposing

    return (moved, new_elf_positions)


def get_bounding_box(elves):
    BIG = 1 << 20
    miny, minx, maxy, maxx = BIG, BIG, -BIG, -BIG
    for x, y in elves:
        miny = min(y, miny)
        minx = min(x, minx)
        maxy = max(y, maxy)
        maxx = max(x, maxx)
    
    return (minx, maxx, miny, maxy)


def generate_new_grid(elves):
    minx, maxx, miny, maxy = get_bounding_box(elves)
    new_grid = [['.'] * (maxx - minx + 1) for _ in range(miny, maxy + 1)]
    for x, y in elves:
        new_grid[y - miny][x - minx] = '#'
    
    return [''.join(row) for row in new_grid]


def main():
    input_lines = sys.stdin.read().split('\n')
    grid = [line.strip() for line in input_lines]
    elves = [(x, y) for (y, row) in enumerate(grid) for (x, cell) in enumerate(row) if cell == '#']
    elves2 = elves[:]
    # part 1
    for i in range(10):
        _, elves = simulate_round(elves, i % 4)

    minx, maxx, miny, maxy = get_bounding_box(elves)
    bounding_area = (maxx - minx + 1) * (maxy - miny + 1)
    free = bounding_area - len(elves)
    print(free)

    # part 2
    for round in range(0, 1000):
        moved, elves2 = simulate_round(elves2, round % 4)
        if not moved:
            print(round + 1)
            break


if __name__ == '__main__':
    main()
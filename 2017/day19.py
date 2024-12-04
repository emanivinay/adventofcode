import sys

DIRECTIONS = [SOUTH, EAST, WEST, NORTH] = [(0, 1), (1, 0), (-1, 0), (0, -1)]

def main():
    grid = [line.rstrip('\n') for line in sys.stdin.readlines()]

    def inside_grid(x, y):
        return not (x < 0 or y < 0 or y >= len(grid) or x >= len(grid[y]) or grid[y][x].isspace())

    x, y, dir = grid[0].index('|'), 0, SOUTH
    letters = []
    steps = 0
    while True:
        cur = grid[y][x]
        if cur.isalpha():
            letters.append(cur)
        elif cur == '+':
            # change direction
            if dir in (NORTH, SOUTH):
                dir = EAST if inside_grid(x + 1, y) else WEST
            else:
                dir = NORTH if inside_grid(x, y - 1) else SOUTH

        # advance in current direction
        dx, dy = dir
        x, y = x + dx, y + dy
        steps += 1
        if not inside_grid(x, y):
            break

    print(''.join(letters), steps)


main()
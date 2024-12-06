import sys
import collections
import itertools
import functools


# (dx, dy)
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
DIRECTION_POINTER_MAP = {
    '^': 0,
    '>': 1,
    'v': 2,
    '<': 3,
}


def main():
    grid = sys.stdin.readlines()
    grid = [list(line.strip()) for line in grid]
    H, W = len(grid), len(grid[0])

    def is_inside_grid(y, x):
        return 0 <= y < H and 0 <= x < W

    gx, gy, gdir = 0, 0, 0
    for y in range(H):
        for x in range(W):
            if grid[y][x] in "^>v<":
                gx, gy, gdir = x, y, DIRECTION_POINTER_MAP[grid[y][x]]
    
    def simulate_guard(gx, gy, gdir):
        visited = [[[-1] * 4 for _ in range(W)] for _ in range(H)]
        # h, w, d
        step = 0
        loop_detected = False
        while is_inside_grid(gy, gx):
            if visited[gy][gx][gdir] >= 0:
                # loop detected
                loop_detected = True
                break
            visited[gy][gx][gdir] = step
            step += 1
            dx, dy = DIRECTIONS[gdir]
            gx2, gy2 = gx + dx, gy + dy
            if is_inside_grid(gy2, gx2) and grid[gy2][gx2] == '#':
                # obstacle, turn 90 degrees.
                gdir = (gdir + 1) % 4
            else:
                gx, gy = gx2, gy2
        return loop_detected, visited

    _, visited = simulate_guard(gx, gy, gdir)
    part1, part2 = 0, 0
    
    for y in range(H):
        for x in range(W):
            if any(v >= 0 for v in visited[y][x]) and grid[y][x] == '.':
                part1 += 1
                grid[y][x] = '#'
                loop_detected, _ = simulate_guard(gx, gy, gdir)
                if loop_detected:
                    part2 += 1
                grid[y][x] = '.'

    print(part1 + 1, part2)


if __name__ == '__main__':
    main()

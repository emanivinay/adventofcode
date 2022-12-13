from collections import deque
import sys

BIG = 1 << 30

def elevation_at(grid, r, c):
    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
        return BIG
    
    c = 'a' if grid[r][c] == 'S' else ('z' if grid[r][c] == 'E' else grid[r][c])
    return ord(c)


def shortest_path(grid, R, C, sy, sx, ey, ex):
    if grid[sy][sx] not in 'Sa':
        return BIG

    queue = deque()
    distance = [[BIG] * C for _ in range(R)]

    def visit(r, c, d, prev_elevation):
        if 0 <= r < R and 0 <= c < C and distance[r][c] > d and elevation_at(grid, r, c) + 1 >= prev_elevation:
            distance[r][c] = d
            queue.append((d, r, c))
    
    visit(ey, ex, 0, 0)
    while queue:
        d, r, c = queue.popleft()
        e = elevation_at(grid, r, c)
        visit(r - 1, c, d + 1, e)
        visit(r, c - 1, d + 1, e)
        visit(r + 1, c, d + 1, e)
        visit(r, c + 1, d + 1, e)
    
    return distance[sy][sx], min(distance[r][c] for r in range(R) for c in range(C) if grid[r][c] in 'Sa')


def main():
    grid = sys.stdin.read().split('\n')
    R = len(grid)
    C = len(grid[0])

    sx, sy, ex, ey = -1, -1, -1, -1
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                sy, sx = r, c
            elif grid[r][c] == 'E':
                ey, ex = r, c
    
    # parts 1 and 2
    print(shortest_path(grid, R, C, sy, sx, ey, ex))


if __name__ == '__main__':
    main()
import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    grid = sys.stdin.read().split('\n')
    grid = [[int(cell) for cell in row] for row in grid]
    H, W = len(grid), len(grid[0])

    ADJACENT = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    def visit(y, x, need_value, bfs_q, visited):
        if y < 0 or x < 0 or y >= H or x >= W or visited[y][x] or need_value != grid[y][x]:
            return
        bfs_q.append((y, x))
        visited[y][x] = True

    part1 = 0
    for y in range(H):
        for x in range(W):
            if grid[y][x] == 0:
                bfs_q = collections.deque()
                visited = [[False] * W for _ in range(H)]
                visit(y, x, 0, bfs_q, visited)
                while bfs_q:
                    y2, x2 = bfs_q.popleft()
                    for dy, dx in ADJACENT:
                        y3, x3 = y2 + dy, x2 + dx
                        visit(y3, x3, grid[y2][x2] + 1, bfs_q, visited)
                
                score = 0
                for y2 in range(H):
                    for x2 in range(W):
                        if visited[y2][x2] and grid[y2][x2] == 9:
                            score += 1
                part1 += score
    
    print(part1)


if __name__ == '__main__':
    main()
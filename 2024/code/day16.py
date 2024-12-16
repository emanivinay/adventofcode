import sys
import collections
import itertools
import functools
import heapq


BIG = 1<<40


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def search(grid, sy, sx, sdir):
    bfs_pq = []
    distance = collections.defaultdict(lambda: BIG)

    def next_in_direction(y, x, d):
        dy, dx = DIRECTIONS[d]
        return y + dy, x + dx

    def can_move(y, x, direction):
        y2, x2 = next_in_direction(y, x, direction)
        return grid[y2][x2] != '#'

    def visit(y, x, d, dist):
        if distance[(y, x, d)] > dist:
            distance[(y, x, d)] = dist
            heapq.heappush(bfs_pq, (dist, y, x, d))

    def move_in_d(y, x, direction, dist):
        if can_move(y, x, direction):
            y2, x2 = next_in_direction(y, x, direction)
            d2 = direction
            visit(y2, x2, d2, dist + 1)
    
    visit(sy, sx, sdir, 0)

    while bfs_pq:
        dist, y, x, dir = heapq.heappop(bfs_pq)
        move_in_d(y, x, dir, dist)
        # turn clockwise or anticlockwise
        visit(y, x, (dir + 1) % 4, dist + 1000)
        visit(y, x, (dir + 3) % 4, dist + 1000)
    
    return distance


def main():
    grid = sys.stdin.read().split('\n')
    H, W = len(grid), len(grid[0])

    sy, sx = -1, -1
    ey, ex = -1, -1
    for y in range(H):
        for x in range(W):
            if grid[y][x] == 'S':
                sy, sx = y, x
            elif grid[y][x] == 'E':
                ey, ex = y, x
    
    # part1
    distance_part1 = search(grid, sy, sx, 0)
    answer_part1 = min(distance_part1[(ey, ex, d)] for d in range(4))
    print(answer_part1)

    backwards = collections.defaultdict(lambda: BIG)
    for d in range(4):
        rd = search(grid, ey, ex, d)
        for y in range(H):
            for x in range(W):
                for dd in range(4):
                    key = (y, x, dd)
                    backwards[key] = min(backwards[key], rd[key])
    
    answer_part2 = 0
    for y in range(H):
        for x in range(W):
            good = False
            for d in range(4):
                d2 = (d + 2) % 4
                if answer_part1 == distance_part1[(y, x, d)] + backwards[(y, x, d2)]:
                    good = True
            answer_part2 += good
    
    print(answer_part2)


if __name__ == '__main__':
    main()


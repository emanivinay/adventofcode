import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    grid = sys.stdin.read().split('\n')
    H, W = len(grid), len(grid[0])
    regions = [[-1] * W for _ in range(H)]

    ADJACENT = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    def visit(y, x, color, region_id, bfs_q):
        if y < 0 or x < 0 or y >= H or x >= W or regions[y][x] >= 0 or grid[y][x] != color:
            return
        regions[y][x] = region_id
        bfs_q.append((y, x))

    def count_disconts(vs):
        prev, prev_i, ret = -100, -1, 0
        for x, i in sorted(vs):
            if prev + 1 != x or prev_i != i:
                ret += 1
            prev, prev_i = x, i
        return ret

    def count_sides(plots):
        horizontal = collections.defaultdict(set)
        vertical = collections.defaultdict(set)
        for y, x in plots:
            for i, (dy, dx) in enumerate(ADJACENT):
                y2, x2 = y + dy, x + dx
                if y2 < 0 or x2 < 0 or y2 >= H or x2 >= W or grid[y2][x2] != grid[y][x]:
                    # this fence is part of a side.
                    if i == 0:
                        vertical[x + 1].add((y, i))
                    elif i == 2:
                        vertical[x].add((y, i))
                    elif i == 1:
                        horizontal[y].add((x, i))
                    else:
                        horizontal[y + 1].add((x, i))
        
        return sum(count_disconts(hs) for hs in horizontal.values()) + sum(count_disconts(vs) for vs in vertical.values())

    region_id = 0
    sides = collections.defaultdict(int)
    for y in range(H):
        for x in range(W):
            if regions[y][x] == -1:
                bfs_q = collections.deque()
                visit(y, x, grid[y][x], region_id, bfs_q)
                plots = set()
                while bfs_q:
                    y2, x2 = bfs_q.popleft()
                    plots.add((y2, x2))
                    for dy, dx in ADJACENT:
                        visit(y2 + dy, x2 + dx, grid[y][x], region_id, bfs_q)
                sides[region_id] = count_sides(plots)
                region_id += 1
    
    area, perimeter = collections.defaultdict(int), collections.defaultdict(int)
    for y in range(H):
        for x in range(W):
            region = regions[y][x]
            area[region] += 1
            for dy, dx in ADJACENT:
                y2, x2 = y + dy, x + dx
                if y2 < 0 or x2 < 0 or y2 >= H or x2 >= W or grid[y2][x2] != grid[y][x]:
                    perimeter[region] += 1

    part1, part2 = 0, 0
    for region, a in area.items():
        part1 += a * perimeter[region]
        part2 += a * sides[region]
    
    print(part1, part2)


if __name__ == '__main__':
    main()
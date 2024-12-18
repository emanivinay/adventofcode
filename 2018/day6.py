import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter, split_by=' '):
    return [type_converter(word) for word in line.split(split_by)]


split_ints = lambda line: split_line_to_type(line, int, ', ')


def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def distances_from(p, coords, least_only=False):
    f = min if least_only else sorted
    return f((distance(p, c), i) for i, c in enumerate(coords))


def sum_distances_from(p, coords):
    return sum(distance(p, c) for c in coords)


def main():
    coords = [split_ints(line) for line in sys.stdin.read().split('\n')]
    N = len(coords)
    M = 500
    infinite_regions = set()
    for x in range(-M, M + 1):
        for y in [M, -M]:
            dists = distances_from((x, y), coords)
            if dists[0][0] < dists[1][0]:
                infinite_regions.add(dists[0][1])
            dists = distances_from((y, x), coords)
            if dists[0][0] < dists[1][0]:
                infinite_regions.add(dists[0][1])
    
    finite_region_areas = collections.defaultdict(int)

    bfs_q = collections.deque()
    visited = set()

    for y in range(-M, M + 1):
        for x in range(-M, M + 1):
            dists = distances_from((x, y), coords)
            sum_dists = sum_distances_from((x, y), coords)
            if sum_dists < 10000:
                bfs_q.append((y, x))
                visited.add((y, x))
            if dists[0][0] < dists[1][0]:
                nearest = dists[0][1]
                if nearest not in infinite_regions:
                    finite_region_areas[nearest] += 1
    
    print(max(finite_region_areas.values()))

    # do a flood-fill starting from sy, sx
    ADJACENT = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    while bfs_q:
        y, x = bfs_q.popleft()
        for dy, dx in ADJACENT:
            y2, x2 = y + dy, x + dx
            if (y2, x2) not in visited and sum_distances_from((x2, y2), coords) < 10000:
                visited.add((y2, x2))
                bfs_q.append((y2, x2))
    
    print(len(visited))


if __name__ == '__main__':
    main()

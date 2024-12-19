import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    falling = [tuple(int(w) for w in line.split(',')) for line in sys.stdin.read().split('\n')]
    H, W = 71, 71
    BIG = 1<<30

    def simulate_n_falls(n):
        corrupted = [[False] * W for _ in range(H)]
        for i in range(n):
            x, y = falling[i]
            corrupted[y][x] = True
        
        ADJACENT = [(0, 1), (-1, 0), (0, -1), (1, 0)]
        bfs_q = collections.deque()
        distance = [[BIG] * W for _ in range(H)]
        
        def visit(y, x, dist):
            if 0 <= y < H and 0 <= x < W and not corrupted[y][x] and distance[y][x] > dist:
                distance[y][x] = dist
                bfs_q.append((y, x))
        
        visit(0, 0, 0)
        while bfs_q:
            y, x = bfs_q.popleft()
            for dy, dx in ADJACENT:
                y2, x2 = y + dy, x + dx
                visit(y2, x2, distance[y][x] + 1)
        
        return distance[H - 1][W - 1]

    lo, hi = 1024, len(falling)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if simulate_n_falls(mid) < BIG:
            lo = mid
        else:
            hi = mid

    print(*falling[hi - 1], sep=',')


if __name__ == '__main__':
    main()

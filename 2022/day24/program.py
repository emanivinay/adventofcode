import sys
import collections
import itertools
import functools
from math import lcm


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


# (r, c)
NEXT_CELL = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]
BLIZZARD_TYPES = {
    'v': (1, 0),
    '^': (-1, 0),
    '>': (0, 1),
    '<': (0, -1),
}

def search(valley, blizzards, R, C, T, source, destination, t_offset=0):
    BIG = 1 << 40
    dist = [[[BIG] * T for _ in range(C)] for _ in range(R)]
    queue = collections.deque()

    def visit(r, c, t, d):
        if r < 0 or c < 0 or r >= R or c >= C or valley[r][c] == '#' or blizzards[r][c][t] > 0:
            return
      
        if dist[r][c][t] <= d:
            return

        dist[r][c][t] = d
        queue.append((r, c, t))
    

    t_offset = t_offset % T
    visit(*source, t_offset, 0)

    while queue:
        r, c, t = queue.popleft()
        d = dist[r][c][t]
        for dr, dc in NEXT_CELL:
            rr, cc, tt = r + dr, c + dc, (t + 1) % T
            visit(rr, cc, tt, d + 1)
    
    ret = BIG
    for t in range(T):
        ret = min(ret, dist[destination[0]][destination[1]][t])
    
    return ret


def main():
    input_lines = sys.stdin.read().split('\n')
    valley = [line.strip() for line in input_lines]

    R = len(valley)
    C = len(valley[0])

    T = (R - 2) * (C - 2)
    blizzards = [[[0] * T for _ in range(C)] for _ in range(R)]

    def adjust(x, l, r):
        if x < l:
            return r
        elif x > r:
            return l
        else:
            return x

    for r in range(R):
        for c in range(C):
            if valley[r][c] in BLIZZARD_TYPES:
                dr, dc = BLIZZARD_TYPES[valley[r][c]]
                rr, cc = r, c
                for t in range(T):
                    blizzards[rr][cc][t] += 1
                    rr, cc = rr + dr, cc + dc
                    rr = adjust(rr, 1, R - 2)
                    cc = adjust(cc, 1, C - 2)
    
    t1 = search(valley, blizzards, R, C, T, (0, 1), (R - 1, C - 2), 0)
    t2 = t1 + search(valley, blizzards, R, C, T, (R - 1, C - 2), (0, 1), t1)
    t3 = t2 + search(valley, blizzards, R, C, T, (0, 1), (R - 1, C - 2), t2)
    print(t3)


if __name__ == '__main__':
    main()
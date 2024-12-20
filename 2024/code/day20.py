import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)

BIG = 1 << 40
ADJACENT = [(0, 1), (-1, 0), (0, -1), (1, 0)]

# state is (x, y, cheat) : 0 -> 0, 1. 1 -> 2, 2 -> 3, 3 -> 3

def main():
    grid = sys.stdin.read().split('\n')
    H, W = len(grid), len(grid[0])

    sy, sx, ey, ex = -1, -1, -1, -1
    for y in range(H):
        for x in range(W):
            if grid[y][x] == 'S':
                sy, sx = y, x
            elif grid[y][x] == 'E':
                ey, ex = y, x
    
    def bfs_with_cheats(sy, sx, cheat_duration=2, in_cheat_mode=False):
        bfs_q = collections.deque()
        distance = collections.defaultdict(lambda: BIG)

        def visit(y, x, cheat_state, dist):
            if y < 0 or x < 0 or y >= H or x >= W:
                return
            if (cheat_state < 1 or cheat_state >= cheat_duration) and grid[y][x] == '#':
                return
            key = (y, x, cheat_state)
            if distance[key] > dist:
                distance[key] = dist
                bfs_q.append(key)
        
        visit(sy, sx, 0, 0)
        while bfs_q:
            y, x, c = bfs_q.popleft()
            dist = distance[(y, x, c)]
            for dy, dx in ADJACENT:
                y2, x2 = y + dy, x + dx
                if c == 0:
                    if not in_cheat_mode:
                        visit(y2, x2, 0, dist + 1)
                    visit(y2, x2, 1, dist + 1)
                elif c < cheat_duration:
                    visit(y2, x2, c + 1, dist + 1)
                elif not in_cheat_mode:
                    visit(y2, x2, c, dist + 1)
        
        return distance
    
    d1 = bfs_with_cheats(sy, sx, 2)
    d2 = bfs_with_cheats(ey, ex, 2)

    honest_distance = d1[(ey, ex, 0)]

    part1 = 0
    for y in range(H):
        for x in range(W):
            # (y, x) is the first cheat point.
            for dy, dx in ADJACENT:
                y2, x2 = y + dy, x + dx
                if y2 < 0 or x2 < 0 or y2 >= H or x2 >= W or grid[y2][x2] == '#':
                    continue
                forward = d1[(y, x, 1)]
                backward = d2[(y2, x2, 1)]
                cheat_distance = forward + backward + 1 if grid[y2][x2] != 'E' else forward + 1
                if cheat_distance < honest_distance:
                    saved = honest_distance - cheat_distance
                    if saved >= 100:
                        part1 += 1

    print(part1)


    original_path = set()
    for y in range(H):
        for x in range(W):
            if d1[(y, x, 0)] + d2[(y, x, 0)] == honest_distance:
                original_path.add((y, x))

    part2 = 0    
    for i, (y, x) in enumerate(original_path):
        for dy in range(-20, 21):
            for dx in range(-20, 21):
                move = abs(dy) + abs(dx)
                if move == 0 or move > 20:
                    continue
                y2, x2 = y + dy, x + dx
                if (y2, x2) in original_path and (y2, x2) != (y, x):
                    new_distance = d1[(y, x, 0)] + d2[(y2, x2, 0)] + move
                    if new_distance < honest_distance:
                        saved = honest_distance - new_distance
                        if saved >= 100:
                            part2 += 1
    print(part2)


if __name__ == '__main__':
    main()

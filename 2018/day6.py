import sys

# x, y and order = E, NE, N, NW, W, SW, S, SE
DIRECTIONS = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]


def sign(x):
    return 1 if x > 0 else (0 if x == 0 else -1)


def direction(dx, dy):
    return DIRECTIONS.index((sign(dx), sign(dy)))


ZERO_BOUND = 10001


def mid(x1, x2):
    if x1 == x2:
        return ZERO_BOUND
    elif x1 > x2:
        dx = x1 - x2
        if dx % 2 == 0:
            return x1 - (dx // 2) + 1
        else:
            return x1 - (dx // 2)
    else:
        dx = x2 - x1
        if dx % 2 == 0:
            return x1 + (dx // 2) - 1
        else:
            return x1 + (dx // 2)


def mid_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    return (direction(dx, dy), mid(x1, x2), mid(y1, y2))


def update(df, old, new):
    if old is None or df == 0:
        return new
    elif new is None:
        return old
    elif df > 0:
        return min(old, new)
    else:
        return max(old, new)


def update_bounding_box(dir, edge, x_new, y_new):
    edge[0] = update(dir[0], edge[0], x_new)
    edge[1] = update(dir[1], edge[1], y_new)


def main():
    points = [[int(w) for w in line.split(', ')] for line in sys.stdin.readlines()]
    N = len(points)

    bounding_edges = [[[None, None] for _ in DIRECTIONS] for _ in points]
    for i in range(N):
        x1, y1 = points[i]
        for j in range(i):
            x2, y2 = points[j]
            dir_ij, x_mid, y_mid = mid_line(x1, y1, x2, y2)
            update_bounding_box(DIRECTIONS[dir_ij], bounding_edges[i][dir_ij], x_mid, y_mid)

            dir_ji, x_mid, y_mid = mid_line(x2, y2, x1, y1)
            update_bounding_box(DIRECTIONS[dir_ji], bounding_edges[j][dir_ji], x_mid, y_mid)
    
    for i in range(N):
        for d in range(8):
            bound = 'x' if (None in bounding_edges[i][d] or ZERO_BOUND in bounding_edges[i][d]) else bounding_edges[i][d]
            print(bound, end=' ')
        print()


main()
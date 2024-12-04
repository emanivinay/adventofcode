import sys
from math import sqrt

POSITIVE_INFINITY = 1
NEGATIVE_INFINITY = -1
CONSTANT = 0


def parse_point(coord_str):
    return [int(w) for w in coord_str[1:-1].split(',')]


def parse_point_line(line):
    p, v, a = [parse_point(tok[2:]) for tok in line.split(', ')]
    return (p, v, a)


def long_term_trajectory(p0, v0, a):
    if a > 0:
        return (POSITIVE_INFINITY, 0)
    elif a < 0:
        return (NEGATIVE_INFINITY, 0)
    else:
        if v0 > 0:
            return (POSITIVE_INFINITY, 0)
        elif v0 < 0:
            return (NEGATIVE_INFINITY, 0)
        else:
            return (CONSTANT, p0)


def manhattan_distance(p, p0=(0, 0, 0)):
    x, y, z = p
    x0, y0, z0 = p0
    return abs(x - x0) + abs(y - y0) + abs(z - z0)


def get_point_position(p, v, a, t):
    px, py, pz = p
    vx, vy, vz = v
    ax, ay, az = a

    tt = t * (t + 1) / 2
    fx = px + vx * t + ax * tt
    fy = py + vy * t + ay * tt
    fz = pz + vz * t + az * tt
    return (fx, fy, fz)


def collision_time(p1, p2):
    (p1x, p1y, p1z), (v1x, v1y, v1z), (a1x, a1y, a1z) = p1
    (p2x, p2y, p2z), (v2x, v2y, v2z), (a2x, a2y, a2z) = p2
    dpx, dvx, dax = p2x - p1x, v2x - v1x, a2x - a1x
    # 2 * dpx + 2 * dvx * t + dax * t * (t + 1) = 0

    A, B, C = 2 * dpx, 2 * dvx, dax
    # A + B * t + C * t * (t + 1) = 0
    # C * T^2 + (B + C) * t + A = 0
    if C == 0:
        if B + C == 0:
            return 0 if A == 0 else -1
        else:
            return (-A) / (B + C)

    discriminant = (B + C) ** 2 - 4 * A * C
    if discriminant < 0:
        return -1
    
    # -(B + C) +/- sqrt(discriminant)
    t1 = (-(B + C) + sqrt(discriminant)) / 2 / C
    t2 = (-(B + C) - sqrt(discriminant)) / 2 / C

    ret = -1
    if t1 >= 0:
        p1t = get_point_position(*p1, t1)
        p2t = get_point_position(*p2, t1)
        if manhattan_distance(p1t, p2t) <= 1e-9:
            if ret < 0 or ret > t1:
                ret = t1
    
    if t2 >= 0:
        p1t = get_point_position(*p1, t2)
        p2t = get_point_position(*p2, t2)
        if manhattan_distance(p1t, p2t) <= 1e-9:
            if ret < 0 or ret > t2:
                ret = t2
    
    return ret


def main():
    points = [parse_point_line(line.strip()) for line in sys.stdin.readlines()]

    # part 1
    long_term_positions = [(manhattan_distance(get_point_position(p, v, a, 10 ** 10)), i) for i, (p, v, a) in enumerate(points)]
    _, i = min(long_term_positions)
    print(i)

    # part 2
    N = len(points)

    collisions = []
    coll_times = [-1] * N

    def set_collision_time(i, t_coll):
        if coll_times[i] < 0 or coll_times[i] > t_coll:
            coll_times[i] = t_coll

    for i in range(N):
        for j in range(i):
            t_collision = collision_time(points[i], points[j])
            if t_collision >= 0:
                set_collision_time(i, t_collision)
                set_collision_time(j, t_collision)
                collisions.append((t_collision, i, j))
    
    # collisions.sort()

    dead = set()
    for t, i, j in collisions:
        if 0 <= coll_times[i] < t or 0 <= coll_times[j] < t:
            continue
        dead.add(i)
        dead.add(j)
    
    print(N - len(dead))

    
    

if __name__ == '__main__':
    main()
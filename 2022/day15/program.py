import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def get_coordinate(token):
    token = token.split('=')[-1]
    if token.endswith(':') or token.endswith(','):
        token = token[:-1]
    return int(token)


def parse_sensor_line(line):
    tokens = line.split()
    sensor_x, sensor_y = get_coordinate(tokens[2]), get_coordinate(tokens[3])
    beacon_x, beacon_y = get_coordinate(tokens[-2]), get_coordinate(tokens[-1])
    return ((sensor_x, sensor_y), (beacon_x, beacon_y))

Y_TO_SCAN = 2000000


def no_beacon_range(sensor, beacon, y_to_scan):
    sx, sy = sensor
    bx, by = beacon

    distance = abs(sx - bx) + abs(sy - by)
    dy = abs(y_to_scan - sy)
    if dy > distance:
        return (0, -1)
    
    dx = distance - dy
    rx1, rx2 = sx - dx, sx + dx
    if (rx1, y_to_scan) == (bx, by):
        rx1 += 1
    if (rx2, y_to_scan) == (bx, by):
        rx2 -= 1
    
    return (rx1, rx2)


def potential_beacon_ranges_on_y(sensor_beacon_pairs, y, clipper=None):
    ranges = []
    for sensor, beacon in sensor_beacon_pairs:
        (x1, x2) = no_beacon_range(sensor, beacon, y)
        if x1 > x2:
            continue
        if clipper:
            x1, x2 = clipper(x1, x2)
        if x1 <= x2:
            ranges.append((x1, x2))
    
    ranges.sort()
    return ranges


def clip_range_to_0_4000000(x1, x2):
    x1 = max(x1, 0)
    x2 = min(x2, 4000000)
    return (x1, x2)


def range_union(ranges):
    ret, left = [], -(1 << 50)
    for x1, x2 in ranges:
        if x1 > left:
            ret.append((x1, x2))
            left = x2
        elif x2 > left:
            a, _ = ret.pop()
            ret.append((a, x2))
            left = x2
    
    return ret


def union_of_no_beacon_zones(sensor_beacon_pairs):
    # in (x + y, x - y) space
    no_beacon_zone_squares = []
    for (sx, sy), (bx, by) in sensor_beacon_pairs:
        D = abs(sx - bx) + abs(sy - by)
        # all (x, y) s.t abs(sx - x) + abs(sy - y) <= D - 1
        # x >= sx, y >= sy => x + y <= sx + sy + D - 1
        # x < sx, y < sy => x + y >= sx + sy - D + 1
        # x >= sx, y < sy => x - sx + sy - y <= D - 1 => x - y <= sx - sy + D - 1
        # otherwise => y - x <= sy - sx + D - 1 => x - y >= sx - sy - (D - 1)
        # sx + sy - (D - 1) <= x + y <= sx + sy + (D - 1)
        # sx - sy - (D - 1) <= x - y <= sx - sy + (D - 1)
        no_beacon_zone = ((sx + sy - (D - 1), sx + sy + (D - 1)), (sx - sy - (D - 1), sx - sy + (D - 1)))
        no_beacon_zone_squares.append(no_beacon_zone)
    
    # Find the union of all these zones
    x_set, y_set = set(), set()
    for (lx, rx), (ly, ry) in no_beacon_zone_squares:
        x_set.add(lx)
        x_set.add(rx + 1)
        y_set.add(ly)
        y_set.add(ry + 1)

    xs = sorted(x_set)
    ys = sorted(y_set)
    n_x = len(xs)
    n_y = len(ys)


def main():
    input_lines = sys.stdin.read().split('\n')
    sensor_beacon_pairs = [parse_sensor_line(line) for line in input_lines]
    beacon_set = set(beacon for (_, beacon) in sensor_beacon_pairs)

    # part1
    ranges = range_union(potential_beacon_ranges_on_y(sensor_beacon_pairs, Y_TO_SCAN))
    print(sum((x2 - x1 + 1) for x1, x2 in ranges))

    # part2
    for y in range(4000001):
        ranges_on_y = range_union(potential_beacon_ranges_on_y(sensor_beacon_pairs, y, clip_range_to_0_4000000))
        if len(ranges_on_y) != 1:
            x = ranges_on_y[0][1] + 1
            if (x, y) not in beacon_set:
                print(x * 4000000 + y, x, y)
                break


if __name__ == '__main__':
    main()

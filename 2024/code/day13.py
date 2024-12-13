import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def parse_button(line):
    _, _, x, y = line.split()
    _, xx = x.strip(",").split('+')
    _, yy = y.split('+')
    return (int(xx), int(yy))


def parse_prize(line):
    _, x, y = line.split()
    _, xx = x.strip(',').split('=')
    _, yy = y.split('=')
    return (int(xx), int(yy))


# A = (a1, a2), B = (b1, b2), P = (p1, p2)
# a2 * x * a1 + a2 * y * b1 = p1 * a2
# a1 * x * a2 + a1 * y * b2 = p2 * a1
# y * (a2 * b1 - a1 * b2) = (p1 * a2 - p2 * a1)
def solve_for(A, B, prize):
    a1, a2 = A
    b1, b2 = B
    p1, p2 = prize

    diff1 = a2 * b1 - a1 * b2
    diff2 = p1 * a2 - p2 * a1
    if diff2 % diff1 != 0:
        return (None, None)
    y = diff2 // diff1
    if y < 0:
        return (None, None)
    # a1 * x + b1 * y = p1
    if (p1 - b1 * y) % a1 != 0:
        return (None, None)
    x = (p1 - b1 * y) // a1
    if x < 0:
        return (None, None)

    return (x, y)


def main():
    input_lines = sys.stdin.read().split('\n')
    machines = []
    i = 0
    while i < len(input_lines):
        button_A = parse_button(input_lines[i])
        button_B = parse_button(input_lines[i + 1])
        prize = parse_prize(input_lines[i + 2])
        i += 4
        machines.append((button_A, button_B, prize))

    part1, part2 = 0, 0
    PART2_OFFSET = 10 ** 13

    for A, B, prize in machines:
        x1, y1 = solve_for(A, B, prize)
        if x1 is not None:
            part1 += 3 * x1 + y1
        
        p1, p2 = prize

        x2, y2 = solve_for(A, B, (PART2_OFFSET + p1, PART2_OFFSET + p2))
        if x2 is not None:
            part2 += 3 * x2 + y2

    print(part1, part2)


if __name__ == '__main__':
    main()

import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    satellites = collections.defaultdict(list)
    parent = dict()
    for line in sys.stdin.read().split('\n'):
        center, orbiting = line.split(')')
        parent[orbiting] = center
        satellites[center].append(orbiting)
    
    def rec(object, depth):
        ret = depth
        for child in satellites[object]:
            ret += rec(child, depth + 1)
        return ret

    def path_to_com(object):
        ret, cur = [], object
        while cur != "COM":
            ret.append(cur)
            cur = parent[cur]
        ret.append("COM")
        return ret[::-1]
    
    print(rec("COM", 0))
    you, santa = parent["YOU"], parent["SAN"]
    your_path = path_to_com(you)
    santas_path = path_to_com(santa)
    i = 0
    while your_path[i] == santas_path[i]:
        i += 1
    part2 = len(your_path) + len(santas_path) - 2 * i
    print(part2)


if __name__ == '__main__':
    main()

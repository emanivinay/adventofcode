import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    input_lines = sys.stdin.read().split('\n')
    if not input_lines[-1]:
        input_lines.pop()
    graph = collections.defaultdict(dict)
    cities = set()
    for line in input_lines:
        words = line.split()
        a, b = words[0], words[2]
        cities.add(a)
        cities.add(b)
        cost = int(words[-1])
        graph[a][b] = cost
        graph[b][a] = cost

    N = len(graph)
    cities = sorted(cities)
    ret, ret2 = 1e60, 0
    for perm in itertools.permutations(range(N)):
        cur, *rest = perm
        cost = 0
        for node in rest:
            cost += graph[cities[cur]][cities[node]]
            cur = node
        ret = min(ret, cost)
        ret2 = max(ret2, cost)
    print(ret, ret2)


if __name__ == '__main__':
    main()

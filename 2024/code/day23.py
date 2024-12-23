import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    edges = collections.defaultdict(list)
    for edge in sys.stdin.read().split('\n'):
        a, b = edge.split('-')
        edges[a].append(b)
        edges[b].append(a)
    
    nodes = sorted(edges.keys())
    node_map = dict((node, i) for i, node in enumerate(nodes))
    
    N = len(nodes)

    def matrix_and_bitmap_forms(edges):
        ret = [[False] * N for _ in range(N)]
        bitmap = [0] * N
        for node, alist in edges.items():
            ai = node_map[node]
            for b in alist:
                bi = node_map[b]
                ret[ai][bi] = ret[bi][ai] = True
                bitmap[ai] |= 1 << bi
                bitmap[bi] |= 1 << ai

        return ret, bitmap

    graph, bitmap = matrix_and_bitmap_forms(edges)

    part1 = 0
    triples = []
    for i in range(N):
        for j in range(i + 1, N):
            if not graph[i][j]:
                continue
            for k in range(j + 1, N):
                if graph[i][k] and graph[j][k]:
                    if nodes[i][0] == 't' or nodes[j][0] == 't' or nodes[k][0] == 't':
                        part1 += 1
                    triples.append([i, j, k])
    
    print(part1)

    best = []

    def recurse(selected, common):
        if common == 0:
            if len(selected) > len(best):
                best.clear()
                best.extend(selected)
            return

        last = selected[-1]
        for i in range(last + 1, N):
            if common & (1 << i):
                selected.append(i)
                recurse(selected, common & bitmap[i])
                selected.pop()
        return

    for a, b, c in triples:
        recurse([a, b, c], bitmap[a] & bitmap[b] & bitmap[c])

    part2 = ','.join(nodes[e] for e in best)
    print(part2)


if __name__ == '__main__':
    main()

import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def floyd_warshall(N, rules):
    reachable = [[False] * N for _ in range(N)]
    for a, b in rules:
        reachable[a][b] = True
    
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if reachable[j][i] and reachable[i][k]:
                    reachable[j][k] = True
    
    return reachable


def main():
    input_lines = sys.stdin.read().split('\n')
    rules_set = set()
    updates = []
    for line in input_lines:
        if '|' in line:
            a, b = line.split('|')
            a, b = int(a), int(b)
            rules_set.add((a, b))
        elif line:
            update = line.split(',')
            update = [int(w) for w in update]
            updates.append(update)
    
    N = 100
    part1, part2 = 0, 0
    for update in updates:
        M = len(update)
        bad_update = False
        for j in range(M):
            for k in range(j):
                if (update[j], update[k]) in rules_set:
                    bad_update = True
        
        if not bad_update:
            part1 += update[M // 2]
        else:
            good_ordering = []
            while len(good_ordering) < M:
                for i in range(M):
                    if update[i] in good_ordering:
                        continue
                    good_to_take = True
                    for j in range(M):
                        if update[j] not in good_ordering and (update[j], update[i]) in rules_set:
                            good_to_take = False
                            break
                    if good_to_take:
                        good_ordering.append(update[i])
                        break
            part2 += good_ordering[M // 2]

    print(part1, part2)


if __name__ == '__main__':
    main()
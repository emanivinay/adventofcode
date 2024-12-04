import sys
from functools import lru_cache


def read_input():
    lines = [line.strip() for line in sys.stdin.readlines()]
    data = [line.split() for line in lines]
    return [(row, [int(t) for t in counts.split(',')])for row, counts in data]


def dp_search_raw_input_line(line):
    row, counts = line.split()
    counts = [int(t) for t in counts.split(',')]
    return dp_search(row, counts)


def dp_search(row, damaged_counts):
    N = len(row)
    M = len(damaged_counts)

    prefix_counts = [0] * (N + 1)
    for i in range(N):
        prefix_counts[i + 1] = prefix_counts[i] + (row[i] == '.')

    @lru_cache(maxsize=None)
    def f(i, j):
        if i >= N:
            return j == M
        ret = 0
        if row[i] == '#' or row[i] == '?':
            # damaged.
            if j == M:
                return 0
            span = damaged_counts[j]
            if i + span > N or prefix_counts[i + span] > prefix_counts[i]:
                return 0
            if i + span == N or row[i + span] != '#':
                ret += f(i + span + 1, j + 1)
        if row[i] == '.' or row[i] == '?':
            ret += f(i + 1, j)

        return ret

    return f(0, 0)


def main():
    data = read_input()
    ret = 0
    for row, damaged_counts in data:
        ret += dp_search('?'.join(row for _ in range(5)), damaged_counts * 5)
    print(ret)


if __name__ == '__main__':
    main()


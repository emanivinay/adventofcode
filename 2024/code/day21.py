import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)

BIG = 1 << 50

DIRECTIONS = {
    'v': (1, 0),
    '^': (-1, 0),
    '<': (0, -1),
    '>': (0, 1)
}

def search_paths(grid):
    H, W = len(grid), len(grid[0])
    ret = collections.defaultdict(list)

    def f(y, x, start, path):
        if len(path) > 5:
            return
        key = start + grid[y][x]
        ret[key].append(path)
        for c, (dy, dx) in DIRECTIONS.items():
            y2, x2 = y + dy, x + dx
            if 0 <= y2 < H and 0 <= x2 < W and grid[y2][x2] != '_':
                f(y2, x2, start, path + c)
    
    for y in range(H):
        for x in range(W):
            if grid[y][x] == '_':
                continue
            f(y, x, grid[y][x], '')

    for val in ret.values():
        val.sort(key=len)
        while val and len(val[-1]) > len(val[0]):
            val.pop()
    return ret


p1 = search_paths(["789", "456", "123", "_0A"])
p2 = search_paths(["_^A", "<v>"])


def dirpad_keyseq_for_digit_pair(d1, d2):
    return p1[d1 + d2]


def dirpad_keyseq_for_code(code):
    dig = 'A'
    ret = ['']
    for c in code:
        ret2 = []
        for inter in dirpad_keyseq_for_digit_pair(dig, c):
            for pref in ret:
                ret2.append(pref + inter + 'A')
        ret = ret2
        dig = c
    return ret


def dirpad_keyseq_for_dirpair(d1, d2):
    return p2[d1 + d2]


def dirpad_keyseq_for_dircode(code):
    dig = 'A'
    ret = ['']
    for c in code:
        ret2 = []
        for inter in dirpad_keyseq_for_dirpair(dig, c):
            for pref in ret:
                ret2.append(pref + inter)
        ret = ret2
        dig = c
    return ret


@functools.lru_cache(maxsize=None)
def f(dkey1, dkey2, keypads):
    if keypads == 0:
        return 1
    
    lower_seqs = dirpad_keyseq_for_dirpair(dkey1, dkey2)
    ret = BIG
    for seq in lower_seqs:
        cur, total = 'A', 0
        for c in seq:
            total += f(cur, c, keypads - 1)
            cur = c
        total += f(cur, 'A', keypads - 1)
        ret = min(ret, total)
    return ret


def min_presses_fast(code, keypads=2):
    ret = BIG
    for first_seq in dirpad_keyseq_for_code(code):
        cur, total = 'A', 0
        for c in first_seq:
            total += f(cur, c, keypads)
            cur = c
        ret = min(ret, total)
    return ret


def main():
    codes = sys.stdin.read().split('\n')
    part1, part2 = 0, 0
    for code in codes:
        code_value = int(code[:-1])
        part1 += min_presses_fast(code) * code_value
        part2 += min_presses_fast(code, 25) * code_value
    
    print(part1, part2)


if __name__ == '__main__':
    main()

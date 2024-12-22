import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


# Num pad layout
# 789
# 456
# 123
# _0A
#
# Dir pad layout
# _^A
# <v>
# D Pad 1 -> D pad 2 -> D pad 3 -> Num pad should press input code

BIG = 1 << 50
DIR_PAD_LAYOUT = dict(((i // 3, i % 3), c) for i, c in enumerate("_^A<v>"))
NUM_PAD_LAYOUT = dict(((i // 3, i % 3), c) for i, c in enumerate("789456123_0A"))

DIRECTIONS = {
    'v': (1, 0),
    '^': (-1, 0),
    '<': (0, -1),
    '>': (0, 1)
}

def are_good_num_pad_coordinates(y, x):
    return (0 <= y < 4) and (0 <= x < 3) and (y, x) != (3, 0)


def are_good_dir_pad_coordinates(y, x):
    return (0 <= y < 2) and (0 <= x < 3) and (y, x) != (0, 0)


def get_numpad_coords_for_digit(d):
    for (y, x), dig in NUM_PAD_LAYOUT.items():
        if dig == d:
            return y, x


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


def gen_next_states(index, locn, ilocs, code, keypads=2):
    if any(not are_good_dir_pad_coordinates(*iloc) for iloc in ilocs):
        return
    if not are_good_num_pad_coordinates(*locn):
        return
    
    # pressing Activate button on our own keypad
    i = 0
    while i < keypads and ilocs[i] == (0, 2):
        i += 1
    
    if i == keypads:
        # numpad is activated.
        if NUM_PAD_LAYOUT[locn] == code[index]:
            yield (index + 1, locn, ilocs)
    else:
        # keypad i is activated.
        dir_key = DIR_PAD_LAYOUT[ilocs[i]]
        dy2, dx2 = DIRECTIONS[dir_key]
        if i == keypads - 1:
            # press a button on numpad
            y2, x2 = (locn[0] + dy2, locn[1] + dx2)
            if are_good_num_pad_coordinates(y2, x2):
                yield (index, (y2, x2), ilocs)
        else:
            # press a button the i + 1 th keypad
            y2, x2 = (ilocs[i + 1][0] + dy2, ilocs[i + 1][1] + dx2)
            if are_good_dir_pad_coordinates(y2, x2):
                new_ilocs = ilocs[:i + 1] + ((y2, x2), ) + ilocs[i + 2:]
                yield (index, locn, new_ilocs)


    # pressing a direction button on our own keypad, moves first iloc
    fy, fx = ilocs[0]
    for dy, dx in DIRECTIONS.values():
        fy2, fx2 = (fy + dy, fx + dx)
        if are_good_dir_pad_coordinates(fy2, fx2):
            new_ilocs = ((fy2, fx2), ) + ilocs[1:]
            yield (index, locn, new_ilocs)


def min_presses(code, keypads=2):
    start = (0, (3, 2), tuple((0, 2) for _ in range(keypads)))
    bfs_q = collections.deque()
    distance = collections.defaultdict(lambda: BIG)
    distance[start] = 0
    bfs_q.append(start)
    while bfs_q:
        state = bfs_q.popleft()
        dst = distance[state]
        if state[0] == len(code):
            return dst
        for next_state in gen_next_states(*state, code, keypads):
            if distance[next_state] > 1 + dst:
                distance[next_state] = 1 + dst
                bfs_q.append(next_state)
    return -1


def main():
    codes = sys.stdin.read().split('\n')
    part1, part2 = 0, 0
    for code in codes:
        code_value = int(code[:-1])
        part1 += min_presses(code) * code_value
        part2 += min_presses_fast(code, 25) * code_value
    
    print(part1, part2)


if __name__ == '__main__':
    main()

import sys
import collections
import itertools
import bisect
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def range_map_lookup(range_map, src_no):
    i = bisect.bisect_right(range_map, (src_no, 0, 0))
    if i == 0:
        return src_no
    i -= 1
    if range_map[i][0] + range_map[i][2] - 1 >= src_no:
        diff = src_no - range_map[i][0]
        return range_map[i][1] + diff
    
    return src_no


def seed_to_loc(seed, range_maps):
    for range_map in range_maps:
        seed = range_map_lookup(range_map, seed)
    return seed


def split_range_by_range_map(range, range_map):
    splits = []
    start, size = range
    cur = start
    for r_start, d_start, r_size in range_map:
        if cur >= start + size:
            break
        if r_start + r_size <= cur:
            continue
        if r_start >= start + size:
            splits.append((cur, start + size - cur))
            break
        if r_start > cur:
            ln = min(r_start - cur, start + size - cur)
            splits.append((cur, ln))
            cur += ln
            continue
        else:
            ln = min()

    return splits


def translate_range_with_range_map(range, range_map):
    ranges = [range]
    return [range for range in split_range_by_range_map(range, range_map)]


def translate_range_with_all_range_maps(range, range_maps):
    ranges = [range]
    for range_map in range_maps:
        ranges = [part for part in translate_range_with_range_map(range, range_map) for range in ranges]
    return ranges


def read_range_map():
    input()
    ranges = []
    while True:
        line = input()
        if not line:
            break
        dst, src, size = [int(w) for w in line.split()]
        ranges.append((src, dst, size))

    ranges.sort()
    return ranges


def main():
    seeds = [int(w) for w in input().split()[1:]]
    input()

    range_maps = [read_range_map() for _ in range(7)]
    
    # part 1
    ret1 = min(seed_to_loc(seed, range_maps) for seed in seeds)
    print(ret1)

    # part 2
    ret2 = 1e80
    for i in range(len(seeds) // 2):
        seed_range = seeds[2 * i: 2 * i + 2]
        final_ranges = translate_range_with_all_range_maps(seed_range, range_maps)
        ret2 = min(ret2, min(x for x, _ in final_ranges))
    print(ret2)



if __name__ == '__main__':
    main()
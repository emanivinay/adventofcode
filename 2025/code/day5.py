import sys
import bisect


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def sort_and_merge_overlapping_ranges(ranges):
    ranges.sort()
    last = -1
    ret = []
    for a, b in ranges:
        if a > last:
            ret.append((a, b))
            last = b
        else:
            ret[-1] = (ret[-1][0], max(b, ret[-1][1]))
            last = ret[-1][1]
    return ret


def main():
    input_lines = sys.stdin.read().split('\n')
    fresh_ranges = []
    ingredients = []
    for line in input_lines:
        if '-' in line:
            a, b = line.split('-')
            new_range = int(a), int(b)
            fresh_ranges.append(new_range)
        elif not line:
            continue
        else:
            ingredients.append(int(line))
    
    fresh_ranges = sort_and_merge_overlapping_ranges(fresh_ranges)
    # part 1
    fresh_count = 0
    for ing in ingredients:
        i = bisect.bisect_left(fresh_ranges, (ing, 0))
        fresh = False
        if i < len(fresh_ranges):
            a, b = fresh_ranges[i]
            if a <= ing <= b:
                fresh = True
        if i - 1 >= 0:
            a, b = fresh_ranges[i - 1]
            if a <= ing <= b:
                fresh = True
        fresh_count += fresh

    print(fresh_count)

    # part 2
    print(sum(b - a + 1 for a, b in fresh_ranges))


if __name__ == '__main__':
    main()

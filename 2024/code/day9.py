import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    data = [int(c) for c in sys.stdin.read().strip()]
    BUFFER_SIZE = 100000
    uncompressed = [-1] * BUFFER_SIZE # -1 is empty block
    file_id, index = 0, 0
    for i, d in enumerate(data):
        if i % 2 == 0:
            for j in range(d):
                uncompressed[index + j] = file_id
            file_id, index = file_id + 1, index + d
        else:
            index += d

    right = index - 1
    for i in range(index):
        if i >= right:
            break
        if uncompressed[i] == -1:
            while right > i and uncompressed[right] == -1:
                right -= 1
            if right == i:
                break
            uncompressed[i] = uncompressed[right]
            uncompressed[right] = -1
            right -= 1

    # part 1
    part1 = 0
    for i in range(index):
        if uncompressed[i] >= 0:
            part1 += i * uncompressed[i]
    print(part1)

    # part 2
    # Should use heap instead of list.
    frees = collections.defaultdict(list)
    all_files = []
    loc = 0
    for i, d in enumerate(data):
        if i % 2 == 0:
            all_files.append((i // 2, loc, d))
        elif d > 0:
            frees[d].append(loc)
        loc += d
    
    for d in frees.keys():
        frees[d] = frees[d][::-1]

    F = len(all_files)
    final_pos = dict()
    file_sizes = dict()
    for i in range(F - 1, -1, -1):
        file_id, loc, size = all_files[i]
        file_sizes[file_id] = size
        best = -1, -1
        for d in range(9, size - 1, -1):
            if frees[d] and frees[d][-1] < loc:
                if best[0] < 0 or best[0] > frees[d][-1]:
                    best = frees[d][-1], d
        if best[0] < 0:
            final_pos[file_id] = loc
        else:
            free_loc, free_size = best
            final_pos[file_id] = free_loc
            left_over_space = free_size - size
            frees[free_size].pop()
            if left_over_space > 0:
                frees[left_over_space].append(best[0] + size)
                frees[left_over_space].sort(reverse=True)

    part2 = 0
    for file_id, begin in final_pos.items():
        size = file_sizes[file_id]
        for i in range(size):
            part2 += (begin + i) * file_id
    print(part2)


if __name__ == '__main__':
    main()
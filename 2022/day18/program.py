import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)

def gen_neighbors(x, y, z):
    yield (x, y, z + 1)
    yield (x, y, z - 1)
    yield (x - 1, y, z)
    yield (x + 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)


def is_trapped(x, y, z, cube_set):
    queue = collections.deque()
    visited = set()
    
    def add(x, y, z):
        key = (x, y, z)
        if key not in visited and key not in cube_set:
            visited.add(key)
            queue.append(key)
    
    add(x, y, z)
    while queue:
        x, y, z = queue.popleft()
        if min(x, y, z) < -1 or max(x, y, z) > 22:
            return False
        
        for xx, yy, zz in gen_neighbors(x, y, z):
            add(xx, yy, zz)
    
    return True


def main():
    input_lines = sys.stdin.read().split('\n')
    cubes = [tuple(int(x) for x in line.strip().split(',')) for line in input_lines]
    
    cube_set = set(cubes)

    # part 1
    area = 0
    for cube in cubes:
        for neighbor in gen_neighbors(*cube):
            if neighbor not in cube_set:
                area += 1
    print(area)

    # part 2
    trapped_set = set()
    for x in range(22):
        for y in range(22):
            for z in range(22):
                if is_trapped(x, y, z, cube_set):
                    trapped_set.add((x, y, z))
    
    area = 0
    for cube in cubes:
        for neighbor in gen_neighbors(*cube):
            if neighbor not in cube_set and neighbor not in trapped_set:
                area += 1
    print(area)

if __name__ == '__main__':
    main()
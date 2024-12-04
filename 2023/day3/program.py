import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def neighbors(R: int, C: int, y: int, x: int):
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if (dx != 0 or dy != 0) and 0 <= y + dy < R and 0 <= x + dx < C:
                yield (y + dy, x + dx)


def is_symbol(c: str):
    return (not c.isdigit()) and c != '.'


def main():
    input_lines = sys.stdin.read().split('\n')
    grid = [line.strip() for line in input_lines]

    R = len(grid)
    C = len(grid[0])
    total_part1 = 0
    gears = collections.defaultdict(list)
    for r in range(R):
        c = 0
        while c < C:
            if grid[r][c].isdigit():
                number, touches_symbol = 0, False
                touching_gears = set()
                while c < C and grid[r][c].isdigit():
                    number = 10 * number + int(grid[r][c])
                    for y, x in neighbors(R, C, r, c):
                        if is_symbol(grid[y][x]):
                            touches_symbol = True
                            if grid[y][x] == '*':
                                touching_gears.add((y, x))
                    c += 1
                if touches_symbol:
                    total_part1 += number
                for gear in touching_gears:
                    gears[gear].append(number)
            else:
                c += 1
    
    print(total_part1)
    total_part2 = 0
    for gear, numbers in gears.items():
        if len(numbers) == 2:
            total_part2 += numbers[0] * numbers[1]
    print(total_part2)


if __name__ == '__main__':
    main()
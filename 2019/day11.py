import sys
from collections import defaultdict
from intcode import simulate_intcode_computer

# UP, LEFT, DOWN, RIGHT = (x, y) coords
DIRECTIONS = [UP, LEFT, DOWN, RIGHT] = [(0, 1), (-1, 0), (0, -1), (1, 0)]

# color codes as defined in the problem statement.
BLACK, WHITE = 0, 1

def simulate_instructor(robot_program):
    x, y, d = 0, 0, 0
    color_map = defaultdict(lambda: BLACK)
    color_map[(x, y)] = WHITE

    def inputter():
        return color_map[(x, y)]
    
    output_turn = 0
    output_values = [0, 0]

    def outputter(val):
        nonlocal output_turn, x, y, d
        output_values[output_turn] = val
        output_turn += 1
        if output_turn == 2:
            output_turn = 0
            color, turn = output_values
            color_map[(x, y)] = color
            turn_by = [1, 3][turn]
            d = (d + turn_by) % 4
            dx, dy = DIRECTIONS[d]
            x, y = x + dx, y + dy

    simulate_intcode_computer(robot_program, inputter, outputter)

    # Paint the final grid, invert the y coordinate if required
    miny = min(y for _, y in color_map.keys())
    maxy = max(y for _, y in color_map.keys())
    minx = min(x for x, _ in color_map.keys())
    maxx = max(x for x, _ in color_map.keys())

    W, H = maxx - minx + 1, maxy - miny + 1
    grid = [['.'] * W for _ in range(H)]
    for (x, y), c in color_map.items():
        grid[maxy - y][x - minx] = '.#'[c]
    
    for row in grid:
        print(''.join(row))


MAX_ROBOT_PROGRAM_SIZE = 1 << 10

def main():
    robot_program = [int(x) for x in sys.stdin.read().split(',')]
    extra_size_needed = max(0, MAX_ROBOT_PROGRAM_SIZE - len(robot_program))
    robot_program += [0] * extra_size_needed
    simulate_instructor(robot_program)


main()
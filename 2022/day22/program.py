import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)

# right, down, left, up
DIRECTIONS_2D = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parse_movement_str(movement):
    val = 0
    moves = []
    for c in movement:
        if c.isdigit():
            val = 10 * val + int(c)
        else:
            moves.append(val)
            val = 0
            moves.append(c)
    
    if val > 0:
        moves.append(val)
    
    return moves


def out_of_bounds(y, x, H, W, grid):
    return y < 0 or x < 0 or y >= H or x >= W or grid[y][x].isspace()


def try_moving1(y, x, direction, grid):
    dx, dy = DIRECTIONS_2D[direction]
    H, W = len(grid), len(grid[0])
    yy, xx = y + dy, x + dx
    if out_of_bounds(yy, xx, H, W, grid):
        # wrap around
        if direction == 0:
            xx = 0
            while grid[y][xx].isspace():
                xx += 1
        elif direction == 1:
            yy = 0
            while grid[yy][x].isspace():
                yy += 1
        elif direction == 2:
            xx = W - 1
            while grid[y][xx].isspace():
                xx -= 1
        else:
            yy = H - 1
            while grid[yy][x].isspace():
                yy -= 1

    # After potential wraparound, try moving one step.
    if grid[yy][xx] == '#':
        # blocker, stop moving
        return (False, y, x, direction)
    else:
        return (True, yy, xx, direction)


# All input sets have same cube layout.
def boundary_cross_map():
    ret = dict()
    ret2 = dict()
    # (x, y) -> (x, y)
    ret[(4, 6)] = lambda x, y: (49, x, -1, 0)
    ret[(4, 1)] = lambda x, y: (49, 49 - y, -1, 0)
    ret[(3, 1)] = lambda x, y: (y, 49, 0, -1)
    ret[(3, 5)] = lambda x, y: (y, 0, 0, 1)
    ret[(6, 4)] = lambda x, y: (y, 49, 0, -1)
    ret[(6, 2)] = lambda x, y: (y, 0, 0, 1)
    ret[(6, 1)] = lambda x, y: (x, 0, 0, 1)
    ret[(5, 3)] = lambda x, y: (0, x, 1, 0)
    ret[(5, 2)] = lambda x, y: (0, 49 - y, 1, 0)
    ret[(2, 6)] = lambda x, y: (0, x, 1, 0)
    ret[(2, 5)] = lambda x, y: (0, 49 - y, 1, 0)
    ret[(1, 3)] = lambda x, y: (49, x, -1, 0)
    ret[(1, 4)] = lambda x, y: (49, 49 - y, -1, 0)
    ret[(1, 6)] = lambda x, y: (x, 49, 0, -1)

    ret2[(1, 1, 0)] = 4
    ret2[(1, 0, 1)] = 3
    ret2[(1, 0, -1)] = 6

    ret2[(2, 0, -1)] = 6
    ret2[(2, -1, 0)] = 5

    ret2[(3, 1, 0)] = 1
    ret2[(3, -1, 0)] = 5

    ret2[(4, 1, 0)] = 1
    ret2[(4, 0, 1)] = 6
    
    ret2[(5, -1, 0)] = 2
    ret2[(5, 0, -1)] = 3

    ret2[(6, 1, 0)] = 4
    ret2[(6, -1, 0)] = 2
    ret2[(6, 0, 1)] = 1

    return ret, ret2


BOUNDARY_CROSS_MAP, NEXT_FACE_MAP = boundary_cross_map()

# x, y
FACE_TOP_LEFT_CORNERS = {
    1: (100, 0),
    2: (50, 0),
    3: (50, 50),
    4: (50, 100),
    5: (0, 100),
    6: (0, 150),
}


def get_face_of_grid_region(x, y):
    for no, (tx, ty) in FACE_TOP_LEFT_CORNERS.items():
        if tx <= x < tx + 50 and ty <= y < ty + 50:
            return no

    return -1


def try_moving2(y, x, direction, grid):
    dx, dy = DIRECTIONS_2D[direction]
    H, W = len(grid), len(grid[0])
    xx, yy = x + dx, y + dy
    if out_of_bounds(yy, xx, H, W, grid):
        face1 = get_face_of_grid_region(x, y)
        face2 = NEXT_FACE_MAP[(face1, dx, dy)]
        face2_tx, face2_ty = FACE_TOP_LEFT_CORNERS[face2]
        xx, yy, dx2, dy2 = BOUNDARY_CROSS_MAP[(face1, face2)](x % 50, y % 50)
        xx, yy = face2_tx + xx, face2_ty + yy
        direction = DIRECTIONS_2D.index((dx2, dy2))
    
    if grid[yy][xx] == '#':
        return (False, y, x, DIRECTIONS_2D.index((dx, dy)))
    else:
        return (True, yy, xx, direction)


def follow_moves(moves, x, y, direction, grid, try_moving):
    for move in moves:
        if move == 'L':
            direction = (direction + 3) % 4
        elif move == 'R':
            direction = (direction + 1) % 4
        else:
            for _ in range(move):
                success, y, x, direction = try_moving(y, x, direction, grid)
                if not success:
                    break
    
    return (x, y, direction)


def main():
    input_lines = sys.stdin.read().split('\n')
    grid = []
    movement = ''
    H, W = 0, 0
    for line in input_lines:
        if '.' in line or '#' in line:
            W = max(W, len(line.rstrip()))
            grid.append(line.rstrip())
            H += 1
        elif 'R' in line:
            movement = line.strip()
    
    # Normalize grid rows
    for i in range(H):
        row = grid[i]
        extra = W - len(row)
        grid[i] = row + (' ' * extra)

    moves = parse_movement_str(movement)
    
    # parts 1 and 2
    for mover in [try_moving1, try_moving2]:
        y, x, direction = 0, grid[0].index('.'), 0
        x, y, direction = follow_moves(moves, x, y, direction, grid, mover)
        print(1000 * y + 4 * x + 1004 + direction)


if __name__ == '__main__':
    main()
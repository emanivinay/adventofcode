import sys


DIRECTION_MAP = {
    'U': (0, -1),
    'D': (0, 1),
    'L': (-1, 0),
    'R': (1, 0),
}

def grid_cells_occupied_by_wire(wire):
    x, y = 0, 0
    cells = set()
    reach_times = dict()
    t = 0
    for move in wire:
        direction = move[0]
        dist = int(move[1:])
        dx, dy = DIRECTION_MAP[direction]
        for d in range(dist):
            t += 1
            x, y = x + dx, y + dy
            cells.add((x, y))
            if (x, y) not in reach_times:
                reach_times[(x, y)] = t
    
    return cells, reach_times


def main():
    wire1, wire2 = [line.strip().split(',') for line in sys.stdin.readlines()]

    cells1, times1 = grid_cells_occupied_by_wire(wire1)
    cells2, times2 = grid_cells_occupied_by_wire(wire2)

    best = -1
    for x, y in cells1 & cells2:
        temp = times1[(x, y)] + times2[(x, y)]
        if best < 0 or best > temp:
            best = temp
    
    print(best)


main()
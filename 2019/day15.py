from collections import defaultdict, deque
from intcode import simulate_intcode_computer

[WALL, FREE, OXYGEN, UNKNOWN] = [0, 1, 2, 3]

# (dx, dy)
DIRECTIONS = [EAST, NORTH, WEST, SOUTH] = [(1, 0), (0, -1), (-1, 0), (0, 1)]

def simulate_repair_droid(robot_program):
    grid_map = defaultdict(lambda: UNKNOWN)

    def get_direction(cur, nxt):
        dx, dy = nxt[0] - cur[0], nxt[1] - cur[1]
        return DIRECTIONS.index((dx, dy))

    def adjust_direction(dir):
        dir %= 4
        return dir if dir > 0 else 4

    def gen_cell_neighbors(cell):
        x, y = cell
        for dx, dy in DIRECTIONS:
            yield (x + dx, y + dy)

    def shortest_path(start, destination):
        queue = deque()
        BIG = 1 << 30
        distance_map = defaultdict(lambda: BIG)
        predecessor_map = dict()

        def visit(cell, d, previous):
            if distance_map[cell] <= d or grid_map[cell] not in (OXYGEN, FREE):
                return
            distance_map[cell] = d
            predecessor_map[cell] = previous
            queue.append(cell)
        
        visit(start, 0, None)

        while queue:
            node = queue.popleft()
            if node == destination:
                break
            d = distance_map[node]
            for neighbor in gen_cell_neighbors(node):
                visit(neighbor, d + 1, node)
        
        path, node = [], destination
        print(start, end=' ')
        while node != start:
            print(node, end=' ')
            path.append(node)
            if node not in predecessor_map:
                print('error')
                break
            node = predecessor_map[node]
        
        return path[::-1]

    BIG = 1 << 50
    distance_map = defaultdict(lambda: BIG)
    neighbor_explore_queue = deque()
    grid_map[(0, 0)] = FREE
    def add_to_explore_queue(cell, cell_type, distance):
        if grid_map[cell] not in (OXYGEN, FREE) or distance_map[cell] <= distance:
            return
        distance_map[cell] = distance
        neighbor_explore_queue.append(cell)

    cur_x, cur_y = 0, 0
    oxy_x, oxy_y = 0, 0
    nxt_x, nxt_y = None, None
    add_to_explore_queue((0, 0), FREE, 0)

    def inputter():
        nonlocal nxt_x, nxt_y
        while neighbor_explore_queue:
            x, y = neighbor_explore_queue.popleft()
            if grid_map[(x, y)] == OXYGEN:
                break
            for int_x, int_y in shortest_path((cur_x, cur_y), (x, y)):
                direction = get_direction((cur_x, cur_y), (int_x, int_y))
                nxt_x, nxt_y = int_x, int_y
                yield adjust_direction(direction)
            
            # Now, cur_x, cur_y = (x, y)

            # Explore all four neighbors of (x, y)
            for d in range(4):
                dx, dy = DIRECTIONS[d]
                nxt_x, nxt_y = x + dx, y + dy
                yield adjust_direction(d)
                if (cur_x, cur_y) != (x, y):
                    nxt_x, nxt_y = x, y
                    yield adjust_direction(d + 2)
        
        while True:
            yield 999

    input_seq = inputter()
    def inputter2():
        return next(input_seq)

    def outputter(val):
        nonlocal oxy_x, oxy_y, cur_x, cur_y
        grid_map[(nxt_x, nxt_y)] = val
        # If desirable, put it on neighbor_explore_queue
        add_to_explore_queue((nxt_x, nxt_y), val, distance_map[(cur_x, cur_y)] + 1)
        if val == OXYGEN:
            oxy_x, oxy_y = nxt_x, nxt_y
        if val != WALL:
            cur_x, cur_y = nxt_x, nxt_y

    simulate_intcode_computer(robot_program, inputter2, outputter)

    # Part 1 - find shortest path from (0, 0) to oxygen
    print('Exploration complete')
    print(distance_map[(oxy_x, oxy_y)])


def main():
    robot_program = [int(x) for x in open('input15.txt').read().split(',')]
    L = len(robot_program)
    extra = (1 << 20) - L
    robot_program += [0] * extra
    simulate_repair_droid(robot_program)


main()
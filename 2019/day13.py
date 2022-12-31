import sys
from intcode import simulate_intcode_computer


TILES = [' ', '#', '*', '_', 'o']


def simulate_arcade_cabinet(arcade_program):
    output_values = []
    game_map = dict()
    special_objects = dict()

    def signum(x):
        return 0 if x == 0 else (-1 if x < 0 else 1)

    def inputter():
        px, _ = special_objects[3]
        bx, _ = special_objects[4]
        return signum(bx - px)
    
    def outputter(val):
        output_values.append(val)
        if len(output_values) == 3:
            x, y, tile_id = output_values
            game_map[(x, y)] = tile_id
            special_objects[tile_id] = (x, y)
            output_values.clear()

    arcade_program[0] = 2
    simulate_intcode_computer(arcade_program, inputter, outputter)
    # print(sum(val == 2 for val in game_map.values()))
    print(game_map[(-1, 0)])


MAX_ARCADE_PROGRAM_SIZE = 1 << 20

def main():
    arcade_program = [int(x) for x in open('input13.txt').read().split(',')]
    extra_size_needed = max(0, MAX_ARCADE_PROGRAM_SIZE - len(arcade_program))
    arcade_program += [0] * extra_size_needed
    simulate_arcade_cabinet(arcade_program)


main()
import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


ROCK_TYPES = [
    ['####'],
    ['.#.', '###', '.#.'],
    ['..#', '..#', '###'],
    ['#', '#', '#', '#'],
    ['##', '##'],
]

MAX_HEIGHT = 20000
ROOM_WIDTH = 7

def get_height_of_topmost_rock(room):
    for i in range(MAX_HEIGHT - 1, -1, -1):
        if '#' in room[i]:
            return i
    
    return -1


def is_free_zone(room, rock, top, left):
    h, w = len(rock), len(rock[0])
    for i in range(h):
        if top - i < 0 or top - i >= MAX_HEIGHT:
            return False
        for j in range(w):
            if left + j < 0 or left + j >= ROOM_WIDTH or (room[top - i][left + j] != '.' and rock[i][j] == '#'):
                return False
    
    return True


def move_to(room, rock, top, left, settle=False):
    h, w = len(rock), len(rock[0])
    if not is_free_zone(room, rock, top, left):
        return False

    if settle:
        for i in range(h):
            for j in range(w):
                if rock[i][j] == '#':
                    room[top - i][left + j] = '#'
    return True


def simulate_rock_fall(room, rock_index, push_sequence, push_seq_index):
    rock = ROCK_TYPES[rock_index[0] % 5]
    h = get_height_of_topmost_rock(room)

    top, left = h + 3 + len(rock), 2
    while True:
        push_dir = push_sequence[push_seq_index[0] % len(push_sequence)]
        push_seq_index[0] += 1
        dx = -1 if push_dir == '<' else 1
        if move_to(room, rock, top, left + dx):
            left += dx
        if move_to(room, rock, top - 1, left):
            top -= 1
        else:
            move_to(room, rock, top, left, True)
            break


def print_room(room):
    h = get_height_of_topmost_rock(room)
    for i in range(h, -1, -1):
        row = ''.join(room[i])
        print(row)
    print('')


def main():
    push_sequence = sys.stdin.read().strip()

    # part 1
    push_seq_index = [0]
    room = [['.'] * ROOM_WIDTH for _ in range(MAX_HEIGHT)]

    rock_index = [0]
    for i in range(2022):
        simulate_rock_fall(room, rock_index, push_sequence, push_seq_index)
        rock_index[0] += 1
    
    h = get_height_of_topmost_rock(room)
    print(h + 1)

    # Here, we observe that after certain number of rocks have fallen, the top row is fully occupied
    # Now this top row acts as the new floor and from here on, the pattern repeats in a cycle.

    # The code only works with my input.
    # at height_index of (713 + 2647 * i), rock_index = (456 + 1710 * i) and push_seq_index = 2628
    MAX = 10 ** 12
    i_max = (MAX - 1 - 456) // 1710
    ht = 713 + 2647 * i_max
    block = 456 + 1710 * i_max
    room = [['.'] * ROOM_WIDTH for _ in range(MAX_HEIGHT)]
    rock_index = [1]
    push_seq_index = [2628]
    for _ in range(block, 10 ** 12):
        simulate_rock_fall(room, rock_index, push_sequence, push_seq_index)
        rock_index[0] += 1

    print(get_height_of_topmost_rock(room) + ht + 2)


if __name__ == '__main__':
    main()
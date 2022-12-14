import collections

CHIPS = 'TPSMRLD'
GENERATORS = 'tpsmrld'

STARTING_FLOORS = [
    'etTpslLdD',
    'PS',
    'mMrR',
    '',
]

CHAR_ENCODING_MAP = {
    't' : 0,
    'T' : 1,
    'p' : 2,
    'P' : 3,
    's' : 4,
    'S' : 5,
    'm' : 6,
    'M' : 7,
    'r' : 8,
    'R' : 9,
    'e' : 10,
    'l' : 11,
    'L' : 12,
    'd' : 13,
    'D' : 14,
}

NUM_PAIRS = len(GENERATORS)
INFINITY = 100
NUM_STATES = 1 << 30
NUM_FLOORS = 4

def get_floor_for_item(state, item):
    return (state >> (2 * CHAR_ENCODING_MAP[item])) & 3


def get_configuration(state):
    generators = [0] * NUM_PAIRS
    chips = [0] * NUM_PAIRS
    generators_on_floor = [0] * NUM_FLOORS
    for i in range(NUM_PAIRS):
        chips[i], generators[i] = get_floor_for_item(state, CHIPS[i]), get_floor_for_item(state, GENERATORS[i])
        generators_on_floor[generators[i]] += 1
    
    return (chips, generators, generators_on_floor)


def get_stuff_on_floor(chips, generators, floor):
    chips_here = ''.join(CHIPS[i] for i in range(NUM_PAIRS) if chips[i] == floor)
    generators_here = ''.join(GENERATORS[i] for i in range(NUM_PAIRS) if generators[i] == floor)
    return chips_here + generators_here


def visualize_state(state):
    chips, generators, _ = get_configuration(state)
    for floor in range(NUM_FLOORS - 1, -1, -1):
        print(get_stuff_on_floor(chips, generators, floor))


def is_dangerous_state(state):
    chips, generators, generators_on_floor = get_configuration(state)
    for i in range(NUM_PAIRS):
        if chips[i] != generators[i] and generators_on_floor[chips[i]] > 0:
            return True
    
    return False


def clear_state_for_char(state, c):
    bit = (2 * CHAR_ENCODING_MAP[c])
    return (state) & (~((1 << bit) | (2 << bit)))


def move_char_to_floor(state, c, new_floor):
    temp_state = clear_state_for_char(state, c)
    bit = (2 * CHAR_ENCODING_MAP[c])
    if new_floor & 1:
        temp_state |= 1 << bit
    if new_floor & 2:
        temp_state |= 2 << bit
    return temp_state


distance = [INFINITY] * NUM_STATES

def gen_state_transitions(state):
    floor = get_floor_for_item(state, 'e')
    chips, generators, _ = get_configuration(state)
    stuff_on_floor = get_stuff_on_floor(chips, generators, floor)
    N_ITEMS = len(stuff_on_floor)
    for i in range(N_ITEMS):
        for j in range(i, N_ITEMS):
            a, b = stuff_on_floor[i], stuff_on_floor[j]
            # move up
            if floor < 3:
                new_state = move_char_to_floor(state, a, floor + 1)
                new_state = move_char_to_floor(new_state, b, floor + 1)
                new_state = move_char_to_floor(new_state, 'e', floor + 1)
                if distance[new_state] == INFINITY and not is_dangerous_state(new_state):
                    yield new_state
            
            if floor >= 1:
                new_state = move_char_to_floor(state, a, floor - 1)
                new_state = move_char_to_floor(new_state, b, floor - 1)
                new_state = move_char_to_floor(new_state, 'e', floor - 1)
                if distance[new_state] == INFINITY and not is_dangerous_state(new_state):
                    yield new_state


def main():
    start_state = 0
    end_state = 0
    for i in range(NUM_FLOORS):
        for c in STARTING_FLOORS[i]:
            start_state += move_char_to_floor(0, c, i)
            end_state += move_char_to_floor(0, c, 3)

    queue = collections.deque([start_state])
    distance[start_state] = 0

    prev_d = -1
    while queue and distance[end_state] == INFINITY:
        state = queue.popleft()
        d = distance[state]
        if d > prev_d:
            prev_d = d
            print(d)
        for next_state in gen_state_transitions(state):
            if distance[next_state] > 1 + d:
                distance[next_state] = 1 + d
                queue.append(next_state)

    print(distance[end_state])


main()
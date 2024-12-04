import sys
import collections
import itertools
import functools

MASK = 0xFFFF

GATES = {
    'NOT': lambda *args: ~args[0] & MASK,
    'OR': lambda *args: args[0] | args[1],
    'AND': lambda *args: args[0] & args[1],
    'LSHIFT': lambda *args: (args[0] << args[1]) & MASK,
    'RSHIFT': lambda *args: (args[0] >> args[1]) & MASK,
    'COPY': lambda *args: args[0],
}

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def parse_wire_line(line: str):
    lhs, out_wire = line.split(' -> ')
    terms = lhs.split()
    # and, or, not, lshift, rshift or copy-line
    if terms[0] == 'NOT':
        return (terms[0], terms[1], out_wire)
    elif len(terms) == 3:
        return (terms[1], terms[0], terms[2], out_wire)
    else:
        # copy line
        return ('COPY', terms[0], out_wire)


def solve_for_wire(wire: str, wiring_map, answer_cache):
    if wire.isdigit():
        return int(wire) & MASK

    if wire in answer_cache:
        return answer_cache[wire]

    gate, inputs = wiring_map[wire]
    inputs = [solve_for_wire(input, wiring_map, answer_cache) for input in inputs]
    ret = GATES[gate](*inputs)
    answer_cache[wire] = ret
    return ret


def main():
    input_lines = sys.stdin.read().split('\n')
    wiring_map = dict()
    for line in input_lines:
        gate, *inputs, out = parse_wire_line(line)
        wiring_map[out] = (gate, inputs)

    # Same code for both parts, only that input wiring needs to be changed for part 2
    print(solve_for_wire('a', wiring_map, dict()))


if __name__ == '__main__':
    main()
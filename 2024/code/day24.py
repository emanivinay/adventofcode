import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


op_table = {
    'OR': lambda x, y: int(x or y),
    'AND': lambda x, y: int(x and y),
    'XOR': lambda x, y: x ^ y,
}

def main():
    compute_graph = dict()
    values = dict()
    gate_output_map = dict()
    for line in sys.stdin.read().split('\n'):
        if ':' in line:
            wire, val = line.split(': ')
            val = int(val)
            values[wire] = val
        elif '->' in line:
            lhs, dest = line.split(' -> ')
            input1, op, input2 = lhs.split()
            compute_graph[dest] = [op, input1, input2]
            gate_output_map[(op, input1, input2)] = dest
            gate_output_map[(op, input2, input1)] = dest
    
    while True:
        changed = False
        for output, deps in compute_graph.items():
            if output in values:
                continue
            op, input1, input2 = deps
            if input1 in values and input2 in values:
                v1 = values[input1]
                v2 = values[input2]
                vo = op_table[op](v1, v2)
                values[output] = vo
                changed = True
        
        if not changed:
            break

    part1 = 0
    for key, val in sorted(values.items(), reverse=True):
        if key[0] == 'z':
            part1 = 2 * part1 + val
    print(part1)


    swapped_gates = []
    def swap_two_gate_outputs(gate1, gate2):
        swapped_gates.append(gate1)
        swapped_gates.append(gate2)
        def f(gate, gate1, gate2):
            if gate not in (gate1, gate2):
                return gate
            return gate1 if gate == gate2 else gate2
        
        new_compute_graph = dict()
        for dest, deps in compute_graph.items():
            op, i1, i2 = deps
            dest2 = f(dest, gate1, gate2)
            new_compute_graph[dest2] = [op, i1, i2]
        

        new_gate_output_map = dict()
        for gate, out in gate_output_map.items():
            dest = f(out, gate1, gate2)
            new_gate_output_map[gate] = dest
        
        return new_compute_graph, new_gate_output_map


    def next_gates(carry_gate, index):
        x_in = f'x{index:02d}'
        y_in = f'y{index:02d}'
        xor_gate_out = gate_output_map[('XOR', x_in, y_in)]
        if carry_gate == '':
            # carry gate for first bit is absent.
            return xor_gate_out, gate_output_map[('AND', x_in, y_in)]

        and_gate_out = gate_output_map[('AND', x_in, y_in)]
        mid_gate_out = gate_output_map[('AND', carry_gate, xor_gate_out)]
        bit_gate_out = gate_output_map[('XOR', xor_gate_out, carry_gate)]
        return bit_gate_out, gate_output_map[('OR', and_gate_out, mid_gate_out)]

    # Run this loop 4 times to get 4 errors pointing to swapped gate outputs.
    carry_gate, i = '', 0
    for i in range(45):
        bit_gate, carry_gate = next_gates(carry_gate, i)
        print(i, bit_gate, carry_gate)

    # After running the loop above 4 times, we see that the following 4 gate output pairs were swapped.
    compute_graph, gate_output_map = swap_two_gate_outputs('rts', 'z07')
    compute_graph, gate_output_map = swap_two_gate_outputs('jpj', 'z12')
    compute_graph, gate_output_map = swap_two_gate_outputs('z26', 'kgj')
    compute_graph, gate_output_map = swap_two_gate_outputs('vvw', 'chv')
    # After fixing these 4 mis-swaps, we see that the above will work correctly if run again now.
    print(','.join(sorted(swapped_gates)))


if __name__ == '__main__':
    main()

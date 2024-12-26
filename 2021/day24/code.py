import sys
import collections
import itertools
import functools

from operator import add, mul, mod

operations = {
    'add': add,
    'mul': mul,
    'div': lambda x, y: x // y,
    'mod': mod
}


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)

def value(registers, arg):
    return registers[arg] if arg in registers else int(arg)


def execute_insts(registers, insts):
    for inst in insts:
        op, dst, *rst = inst
        if op in operations:
            func = operations[op]
            a, b = value(registers, dst), value(registers, rst[0])
            registers[dst] = func(a, b)
        elif op == 'eql':
            arg = value(registers, rst[0])
            registers[dst] = int(arg == registers[dst])
        else:
            # input operation, won't be found
            pass


def main():
    instructions = [line.split() for line in sys.stdin.read().split('\n')]
    instr_sets = [instructions[i * 18 + 1 : i * 18 + 18] for i in range(14)]

    states = {
        0: (),
    }

    for i in range(14):
        new_states = set()
        for z, ws in states:
            for w in range(1, 10):
                registers = dict(w=w, x=0, y=0, z=z)
                execute_insts(registers, instr_sets[i])
                new_states.add((registers['z'], ws + (w,)))
        states = new_states


if __name__ == '__main__':
    main()

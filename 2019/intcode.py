import sys
from operator import add, mul

INTCODE_BINARY_OPERATOR_MAP = {
    1: add,
    2: mul,
}


def get_parameter_mode(opcode, param_pos):
    # 0 <= param_pos < number_args for given opcode
    return (opcode // (10 ** (param_pos + 2))) % 10


def get_parameter_value(program, param, param_mode):
    return program[param] if param_mode == 0 else param


def simulate_intcode_computer(program):
    i = 0
    while i < len(program):
        opcode = program[i]
        op = opcode % 100
        if op == 99:
            break

        if op in INTCODE_BINARY_OPERATOR_MAP:
            a, b, c = program[i + 1 : i + 4]
            pm0, pm1 = get_parameter_mode(opcode, 0), get_parameter_mode(opcode, 1)
            pv0, pv1 = get_parameter_value(program, a, pm0), get_parameter_value(program, b, pm1)
            program[c] = INTCODE_BINARY_OPERATOR_MAP[op](pv0, pv1)
            i += 4
        elif op == 3:
            # Read a single integer from stdin
            a = program[i + 1]
            program[a] = int(input().strip())
            i += 2
        elif op == 4:
            # output a string to stdout in a line by itself
            a = program[i + 1]
            pm0 = get_parameter_mode(opcode, 0)
            pv0 = get_parameter_value(program, a, pm0)
            print(pv0)
            i += 2
        elif op in (5, 6):
            # jump if true/false
            a, b = program[i + 1: i + 3]
            pm0, pm1 = get_parameter_mode(opcode, 0), get_parameter_mode(opcode, 1)
            pv0, pv1 = get_parameter_value(program, a, pm0), get_parameter_value(program, b, pm1)
            if (op == 5) ^ (pv0 == 0):
                i = pv1
            else:
                i += 3
        elif op in (7, 8):
            a, b, c = program[i + 1: i + 4]
            pm0, pm1 = get_parameter_mode(opcode, 0), get_parameter_mode(opcode, 1)
            pv0, pv1 = get_parameter_value(program, a, pm0), get_parameter_value(program, b, pm1)
            program[c] = 1 if ((op == 7 and pv0 < pv1) or (op == 8 and pv0 == pv1)) else 0
            i += 4
        else:
            assert False
from operator import add, mul

INTCODE_OPERATOR_MAP = {
    1: add,
    2: mul,
}

def simulate_intcode_computer(program):
    i = 0
    while i < len(program):
        op = program[i]
        if op == 99:
            break

        input1, input2, output = program[i + 1], program[i + 2], program[i + 3]
        if op in INTCODE_OPERATOR_MAP:
            program[output] = INTCODE_OPERATOR_MAP[op](program[input1], program[input2])
        else:
            assert False
        
        i += 4
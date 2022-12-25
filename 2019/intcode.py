def simulate_intcode_computer(program):
    i = 0
    while i < len(program):
        op = program[i]
        if op == 99:
            break

        input1, input2, output = program[i + 1: i + 4]
        if op == 1:
            program[output] = program[input1] + program[input2]
        elif op == 2:
            program[output] = program[input1] * program[input2]
        else:
            assert False
        
        i += 4
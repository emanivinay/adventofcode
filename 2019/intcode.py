import sys
from operator import add, mul
from threading import Thread
from queue import SimpleQueue


INTCODE_BINARY_OPERATOR_MAP = {
    1: add,
    2: mul,
}

def get_parameter_mode(opcode, param_pos):
    # 0 <= param_pos < number_args for given opcode
    return (opcode // (10 ** (param_pos + 2))) % 10


def get_parameter_value(program, param, param_mode, relative_base, input_param=True):
    if param_mode == 1:
        return param
    elif param_mode == 0:
        return program[param] if input_param else param
    else:
        return program[param + relative_base[0]] if input_param else (param + relative_base[0])


def stdin_inputter():
    return int(input().strip())


def stdout_outputter(value):
    print(value)


class IntcodeComputer:
    def __init__(self, name, program, input_q: SimpleQueue, output_q: SimpleQueue, exiter):
        self.program = program
        self.name = name
        self.exiter = exiter
        self.input_q = input_q
        self.output_q = output_q
        self.relative_base = [0]
    
    def inputter(self):
        ret = self.input_q.get()
        return ret

    def outputter(self, value):
        print(f'{self.name} sending output')
        self.output_q.put(value)

    def simulate(self):
        thread = Thread(target=self._run)
        thread.start()

    def _run(self):
        i = 0
        program, outputter, inputter = self.program, self.outputter, self.inputter
        relative_base = self.relative_base
        while i < len(program):
            opcode = program[i]
            op = opcode % 100
            if op == 99:
                break

            if op in INTCODE_BINARY_OPERATOR_MAP:
                a, b, c = program[i + 1 : i + 4]
                pm0, pm1, pm2 = get_parameter_mode(opcode, 0), get_parameter_mode(opcode, 1), get_parameter_mode(opcode, 2)
                pv0, pv1, pv2 = get_parameter_value(program, a, pm0, relative_base), get_parameter_value(program, b, pm1, relative_base),\
                    get_parameter_value(program, c, pm2, relative_base, False)
                program[pv2] = INTCODE_BINARY_OPERATOR_MAP[op](pv0, pv1)
                i += 4
            elif op == 3:
                # Read a single integer from stdin
                a = program[i + 1]
                pm0 = get_parameter_mode(opcode, 0)
                pv0 = get_parameter_value(program, a, pm0, relative_base, False)
                program[pv0] = inputter()
                # Hack to stop vm for day15 problem.
                if program[pv0] == 999:
                    break
                i += 2
            elif op == 4:
                # output a string to stdout in a line by itself
                a = program[i + 1]
                pm0 = get_parameter_mode(opcode, 0)
                pv0 = get_parameter_value(program, a, pm0, relative_base)
                outputter(pv0)
                i += 2
            elif op in (5, 6):
                # jump if true/false
                a, b = program[i + 1: i + 3]
                pm0, pm1 = get_parameter_mode(opcode, 0), get_parameter_mode(opcode, 1)
                pv0, pv1 = get_parameter_value(program, a, pm0, relative_base), get_parameter_value(program, b, pm1, relative_base)
                if (op == 5) ^ (pv0 == 0):
                    i = pv1
                else:
                    i += 3
            elif op in (7, 8):
                a, b, c = program[i + 1: i + 4]
                pm0, pm1, pm2 = get_parameter_mode(opcode, 0), get_parameter_mode(opcode, 1), get_parameter_mode(opcode, 2)
                pv0, pv1, pv2 = get_parameter_value(program, a, pm0, relative_base), get_parameter_value(program, b, pm1, relative_base),\
                    get_parameter_value(program, c, pm2, relative_base, False)
                program[pv2] = 1 if ((op == 7 and pv0 < pv1) or (op == 8 and pv0 == pv1)) else 0
                i += 4
            elif op == 9:
                a = program[i + 1]
                pm0 = get_parameter_mode(opcode, 0)
                pv0 = get_parameter_value(program, a, pm0, relative_base)
                relative_base[0] += pv0
                i += 2
    
        if self.exiter:
            print(f'{self.name} exiting')
            self.exiter()


def simulate_intcode_computer(program, inputter=stdin_inputter, outputter=stdout_outputter, exiter=None):
    relative_base = [0]

    i = 0
    while i < len(program):
        opcode = program[i]
        op = opcode % 100
        if op == 99:
            break

        if op in INTCODE_BINARY_OPERATOR_MAP:
            a, b, c = program[i + 1 : i + 4]
            pm0, pm1, pm2 = get_parameter_mode(opcode, 0), get_parameter_mode(opcode, 1), get_parameter_mode(opcode, 2)
            pv0, pv1, pv2 = get_parameter_value(program, a, pm0, relative_base), get_parameter_value(program, b, pm1, relative_base),\
                get_parameter_value(program, c, pm2, relative_base, False)
            program[pv2] = INTCODE_BINARY_OPERATOR_MAP[op](pv0, pv1)
            i += 4
        elif op == 3:
            # Read a single integer from stdin
            a = program[i + 1]
            pm0 = get_parameter_mode(opcode, 0)
            pv0 = get_parameter_value(program, a, pm0, relative_base, False)
            program[pv0] = inputter()
            # Hack to stop vm for day15 problem.
            if program[pv0] == 999:
                break
            i += 2
        elif op == 4:
            # output a string to stdout in a line by itself
            a = program[i + 1]
            pm0 = get_parameter_mode(opcode, 0)
            pv0 = get_parameter_value(program, a, pm0, relative_base)
            outputter(pv0)
            i += 2
        elif op in (5, 6):
            # jump if true/false
            a, b = program[i + 1: i + 3]
            pm0, pm1 = get_parameter_mode(opcode, 0), get_parameter_mode(opcode, 1)
            pv0, pv1 = get_parameter_value(program, a, pm0, relative_base), get_parameter_value(program, b, pm1, relative_base)
            if (op == 5) ^ (pv0 == 0):
                i = pv1
            else:
                i += 3
        elif op in (7, 8):
            a, b, c = program[i + 1: i + 4]
            pm0, pm1, pm2 = get_parameter_mode(opcode, 0), get_parameter_mode(opcode, 1), get_parameter_mode(opcode, 2)
            pv0, pv1, pv2 = get_parameter_value(program, a, pm0, relative_base), get_parameter_value(program, b, pm1, relative_base),\
                get_parameter_value(program, c, pm2, relative_base, False)
            program[pv2] = 1 if ((op == 7 and pv0 < pv1) or (op == 8 and pv0 == pv1)) else 0
            i += 4
        elif op == 9:
            a = program[i + 1]
            pm0 = get_parameter_mode(opcode, 0)
            pv0 = get_parameter_value(program, a, pm0, relative_base)
            relative_base[0] += pv0
            i += 2

    if exiter:
        exiter()

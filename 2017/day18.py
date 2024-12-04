import sys
from collections import defaultdict

class TapeProgram:
    pass


def parse_instruction_line(line):
    op, *args = line.split()
    args = [(arg if arg.isalpha() else int(arg)) for arg in args]
    return (op, *args)


def main():
    instructions = [parse_instruction_line(line.strip()) for line in sys.stdin.readlines()]
    registers = defaultdict(int)

    def value(x):
        return registers[x] if isinstance(x, str) else x

    assign_operations_map = {
        'set': lambda _, y: value(y),
        'add': lambda x, y: value(x) + value(y),
        'mul': lambda x, y: value(x) * value(y),
        'mod': lambda x, y: value(x) % value(y),
    }

    iptr, last_played = 0, None
    while 0 <= iptr < len(instructions):
        op, *args = instructions[iptr]
        if op == 'snd':
            last_played = value(args[0])
        elif op in assign_operations_map:
            registers[args[0]] = assign_operations_map[op](args[0], args[1])
        elif op == 'rcv':
            if value(args[0]) != 0:
                print('received', last_played)
                break
        else:
            # jgz
            if value(args[0]) > 0:
                iptr += value(args[1]) - 1

        iptr += 1


if __name__ == '__main__':
    main()
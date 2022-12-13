import sys


def register_index(letter):
    return ord(letter) - ord('a')


def get_reg_or_const(letter, registers):
    if letter in 'abcd':
        return registers[register_index(letter)]
    return int(letter)


def simulator(instrs):
    pc, regs = 0, [0, 0, 1, 0]
    count = 0
    while 0 <= pc < len(instrs):
        instr = instrs[pc]
        count += 1
        if instr[0] == 'inc' or instr[0] == 'dec':
            reg = register_index(instr[1])
            regs[reg] += 1 if instr[0] == 'inc' else -1
            pc += 1
        elif instr[0] == 'cpy':
            value = get_reg_or_const(instr[1], regs)
            dest_reg = register_index(instr[2])
            regs[dest_reg] = value
            pc += 1
        else:
            # jnz instruction
            test_value = get_reg_or_const(instr[1], regs)
            jump_by = int(instr[2])
            if test_value != 0:
                pc += jump_by
            else:
                pc += 1

    print(count)
    return regs


def main():
    instrs = [line.split() for line in sys.stdin.readlines()]
    regs = simulator(instrs)
    print(*regs)


main()

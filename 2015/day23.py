import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)

def even(x):
     return x % 2 == 0

def one(x):
     return x == 1

def halve(x):
     return x // 2

def triple(x):
     return x * 3

def inc(x):
     return x + 1


def parse_program_line(line):
     instr, *args = line.split()
     if instr == 'jmp':
          return ('jmp', lambda reg: True, 'a', int(args[0]))
     elif instr in ('jie', 'jio'):
          f = even if instr == 'jie' else one
          return ('jmp', f, args[0].strip(','), int(args[1]))
     else:
          func = halve if instr == 'hlf' else (triple if instr == 'tpl' else inc)
          return ('mod', func, args[0].strip(','))


def main():
    program = [parse_program_line(line) for line in sys.stdin.read().split('\n')]
    registers = dict(a=0, b=0)
    iptr = 0
    cnt = 0
    while 0 <= iptr < len(program):
        cnt += 1
        instr, f, *rst = program[iptr]
        if instr == 'jmp':
            reg, offset = rst
            if f(registers[reg]):
                iptr += offset
            else:
                iptr += 1
        else:
            reg = rst[0]
            registers[reg] = f(registers[reg])
            iptr += 1

    print(registers['b'], cnt)


if __name__ == '__main__':
    main()

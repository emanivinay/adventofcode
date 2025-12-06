import sys
import collections
import itertools
import functools
from operator import add, mul


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    lines = sys.stdin.read().split('\n')
    grid = [line.split() for line in lines]
    problems = list(zip(*grid))
    # part 1
    total = 0
    def reduce(args, op):
        func = add if op == '+' else mul
        initial = 0 if op == '+' else 1
        return functools.reduce(func, args, initial=initial)

    for problem in problems:
        *args, op = problem
        args = [int(arg) for arg in args]
        total += reduce(args, op)
    print(total)

    # part 2
    def parse_input_line(line):
        words = []
        N = len(line)
        i = 0
        while i < N:
            if line[i].isspace():
                i += 1
                continue
            j = i
            value = 0
            while j < N and line[j].isdigit():
                value = 10 * value + int(line[j])
                j += 1
            
            words.append((i, j - 1, value))
            i = j
        return words
    
    inputs = [parse_input_line(line) for line in lines[:-1]]
    operations = lines[-1].split()
    inputs = list(zip(*inputs))

    def f(inputs, operation):
        towers = collections.defaultdict(list)
        for l, _, val in inputs:
            s = str(val)
            for i, c in enumerate(s, start=l):
                towers[i].append(int(c))
        
        args = []
        for tower in towers.values():
            val = 0
            for d in tower:
                val = 10 * val + d
            args.append(val)
        
        return reduce(args, operation)

    total = sum(f(input, operation) for input, operation in zip(inputs, operations))
    print(total)


if __name__ == '__main__':
    main()

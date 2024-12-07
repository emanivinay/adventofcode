import sys
import collections
import itertools
import functools

from intcode import simulate_intcode_computer


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)

class AmplifierInputter:
    def __init__(self, phase, input):
        self.values = [phase, input]
        self.n_read = 0
    
    def __call__(self):
        ret = self.values[self.n_read]
        self.n_read += 1
        return ret


class AmplifierOutputter:
    def __call__(self, *args):
        self.output = args[0]


def main():
    program = [int(x) for x in sys.stdin.read().split(',')]
    max_output = 0
    for perm in itertools.permutations(range(5)):
        cur_input = 0
        for i in range(5):
            outputter = AmplifierOutputter()
            simulate_intcode_computer(program, AmplifierInputter(perm[i], cur_input), outputter)
            cur_input = outputter.output

        max_output = max(max_output, cur_input)
    print(max_output)


if __name__ == '__main__':
    main()
import sys
import collections
import itertools
import functools
from queue import SimpleQueue
from threading import Semaphore


from intcode import simulate_intcode_computer, IntcodeComputer


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

    # part 2
    for perm in itertools.permutations(range(5, 10)):
        sem = Semaphore(0)
        print(*perm)
        q0, q1, q2, q3, q4 = [SimpleQueue() for _ in range(5)]
        qs = [q0, q1, q2, q3, q4, q0]
        q0.put(0)
        for i, (qi, qo, p) in enumerate(zip(qs, qs[1:], perm)):
            qi.put(p)

            def exiter(release=False):
                if release:
                    sem.release()

            release_sem = i == 4
            name = f'Queue {i}'
            c = IntcodeComputer(name, program, qi, qo, lambda: exiter(release_sem))
            c.simulate()
        
        print('before sem acquiring')
        sem.acquire()
        print('sem acquired')
        print(q0.get())


if __name__ == '__main__':
    main()
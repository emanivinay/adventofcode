import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def parse_monkey_line(line):
    tokens = line.split()
    name = tokens[0][:-1]

    if len(tokens) == 2:
        return (name, int(tokens[1]))
    
    operation = tokens[2]
    dep1 = tokens[1]
    dep2 = tokens[3]

    return (name, operation, [dep1, dep2])


class Value:
    def __init__(self, coeff, const):
        self.coeff = coeff
        self.const = const
    
    def __str__(self):
        return f'{self.coeff}x+{self.const}'
    

    def operate(self, other, operation):
        x1, c1 = self.coeff, self.const
        x2, c2 = other.coeff, other.const

        if operation == '+':
            return Value(x1 + x2, c1 + c2)
        elif operation == '-':
            return Value(x1 - x2, c1 - c2)
        elif operation == '*':
            # Given graph is a tree, only one of them is a variable
            return Value(x1 * c2 + x2 * c1, c1 * c2)
        else:
            assert x2 == 0 and c2 != 0
            return Value(x1 * 1.0 / c2, c1 * 1.0 / c2)


def main():
    input_lines = sys.stdin.read().split('\n')
    monkeys = [parse_monkey_line(line.strip()) for line in input_lines]

    monkey_map = dict()
    for monkey in monkeys:
        name, *args = monkey
        monkey_map[name] = args

    # part 1
    dp_cache = dict()

    def f(name):
        args = monkey_map[name]
        if name in dp_cache:
            return dp_cache[name]

        if name == 'humn':
            dp_cache[name] = Value(1, 0)
            return dp_cache[name]
        
        if len(args) == 1:
            dp_cache[name] = Value(0, args[0])
            return dp_cache[name]
        
        oper, [d1, d2] = args
        v1 = f(d1)
        v2 = f(d2)
        
        dp_cache[name] = v1.operate(v2, oper)
        return dp_cache[name]
    
    # part 1
    # print(f('root'))

    # This is a tree graph of algebraic expressions, with root at 'root'
    # let x be the value that 'humn' should yell.
    # First evaluate the two children of root and get their values as linear functions of 'x'
    d1, d2 = monkey_map['root'][1]

    # Now equate these two linear expressions and solve for x.
    # ax + b = cx + d
    a, b = f(d1).coeff, f(d1).const
    c, d = f(d2).coeff, f(d2).const

    x = (d - b) / (a - c)
    print(x)


if __name__ == '__main__':
    main()
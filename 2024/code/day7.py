import sys
import collections
import itertools
import functools


from operator import mul, add


def concat(lhs, rhs):
    t = 1
    while t <= rhs:
        t *= 10
        lhs *= 10
    return lhs + rhs

OPERATORS_WITHOUT_CONCAT = [add, mul]
OPERATORS_WITH_CONCAT = [add, mul, concat]


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def can_form_target_using_numbers(target, numbers, concat_allowed=False):
    N = len(numbers)
    OPERATORS = OPERATORS_WITH_CONCAT if concat_allowed else OPERATORS_WITHOUT_CONCAT
    NUM_OPS = len(OPERATORS)
    for comb in range(NUM_OPS ** (N - 1)):
        result = numbers[0]
        temp = comb
        for i in range(N - 1):
            op = OPERATORS[temp % NUM_OPS]
            temp = temp // NUM_OPS
            operand = numbers[i + 1]
            result = op(result, operand)
            if result > target:
                break
        if result == target:
            return True
    return False


def main():
    lines = sys.stdin.read().split('\n')
    part1, part2 = 0, 0
    for line in lines:
        lhs, rhs = line.split(': ')
        target = int(lhs)
        numbers = [int(x) for x in rhs.split(' ')]
        if can_form_target_using_numbers(target, numbers):
            part1 += target
        if can_form_target_using_numbers(target, numbers, True):
            part2 += target

    print(part1, part2)


if __name__ == '__main__':
    main()
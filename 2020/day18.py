import sys

def handle_mul_operator1(level, last_operand, number):
    level[-1] = (last_operand * number, '*')


def handle_mul_operator2(level, _, number):
    level.append((number, None))


def add_number_to_level(level, number, handle_mul_operator):
    last_operand, last_operator = level[-1]
    if last_operator == '+':
        level[-1] = (last_operand + number, last_operator)
    elif last_operator == '*':
        handle_mul_operator(level, last_operand, number)
    else:
        # this is the first number at this level.
        level[-1] = (number, None)


# Works both for first and second parts
def calculate_level_value(level):
    ret = 1
    for v, _ in level:
        ret *= v
    return ret


def evaluate_expression(expr, handle_mul_operator):
    add_number_to_level3 = lambda level, number: add_number_to_level(level, number, handle_mul_operator)

    levels = [[(-1, -1)]]

    # all single digit numbers in expressions
    for c in expr:
        if c == '(':
            levels.append([(-1, None)])
        elif c == ')':
            # close and pop this level.
            popped_value = calculate_level_value(levels.pop())
            add_number_to_level3(levels[-1], popped_value)
        elif c.isdigit():
            add_number_to_level3(levels[-1], int(c))
        elif c in '+*':
            level = levels[-1]
            last_operand = level[-1][0]
            level[-1] = (last_operand, c)

    return calculate_level_value(levels[0])


def main():
    expressions = [line.strip() for line in sys.stdin.readlines()]

    # part 1
    print(sum(evaluate_expression(expr, handle_mul_operator1) for expr in expressions))

    # part 2
    print(sum(evaluate_expression(expr, handle_mul_operator2) for expr in expressions))


main()
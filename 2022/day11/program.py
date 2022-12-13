from operator import add, mul
import sys

PRIME_LCM = 2 * 3 * 5 * 7 * 11 * 13 * 17 * 19


def parse_monkey_lines(lines):
    items = [int(t) for t in lines[0].split(': ')[1].split(', ')]
    a, operator, b = lines[1].split(' = ')[1].split()
    OPERATOR_MAP = {
        '+': add,
        '*': mul,
    }
    operation = lambda old: OPERATOR_MAP[operator](old, old if b == 'old' else int(b))
    test_divisor = int(lines[2].split()[-1])
    test_succ_recpt = int(lines[3].split()[-1])
    test_fail_recpt = int(lines[4].split()[-1])
    return (items, operation, test_divisor, test_succ_recpt, test_fail_recpt)


def simulate_n_rounds(n, monkeys):
    M = len(monkeys)
    inspected = [0] * M

    for _ in range(n):
        for i in range(M):
            items, op, testd, s, f = monkeys[i]
            while items:
                old = items.pop(0)
                inspected[i] += 1
                new = op(old) % PRIME_LCM
                to = [f, s][new % testd == 0]
                monkeys[to][0].append(new)

    return inspected


def main():
    input_lines = sys.stdin.read().split('\n')
    monkeys = []
    for i in range(len(input_lines)):
        if input_lines[i].startswith('Monkey'):
            monkeys.append(parse_monkey_lines(input_lines[i + 1 : i + 6]))

    inspected = simulate_n_rounds(10000, monkeys)
    a, b = sorted(inspected, reverse=True)[:2]
    print(a * b)


if __name__ == '__main__':
    main()
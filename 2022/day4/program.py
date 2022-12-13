import sys


def parse_input_lines(lines):
    return [[tuple(int(w) for w in word.split('-')) for word in line.split(',')] for line in lines]


def intersection(r1, r2):
    a1, b1, a2, b2 = *r1, *r2
    return (max(a1, a2), min(b1, b2))


def solve(input_pairs, checker):
    return sum(checker(r1, r2) for r1, r2 in input_pairs)


def checker1(r1, r2):
    return intersection(r1, r2) in [r1, r2]


def checker2(r1, r2):
    a, b = intersection(r1, r2)
    return a <= b


def main():
    input_pairs = parse_input_lines(line.strip() for line in sys.stdin.readlines())
    for checker in [checker1, checker2]:
        print(solve(input_pairs, checker))


if __name__ == '__main__':
    main()
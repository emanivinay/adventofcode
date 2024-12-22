import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def mix(secret, x):
    return secret ^ x


def prune(secret):
    return secret % (1<<24)


def gen_secret_sequence(secret):
    while True:
        yield secret
        secret = mix(secret, secret * 64)
        secret = prune(secret)
        secret = mix(secret, secret // 32)
        secret = mix(secret, secret * 2048)
        secret = prune(secret)


def main():
    buyers = [int(w) for w in sys.stdin.read().split('\n')]
    part1 = 0

    ones_digit_tpl_map = collections.defaultdict(int)

    for buyer in buyers:
        seq = gen_secret_sequence(buyer)
        last_4, last_ones_digit = [], 0
        seen = set()
        for i in range(2001):
            secret = next(seq)
            ones_digit = secret % 10
            if i > 0:
                diff = ones_digit - last_ones_digit
                last_4.append(diff)
            last_ones_digit = ones_digit
            if i >= 4:
                key = tuple(last_4[-4:])
                if key not in seen:
                    seen.add(key)
                    ones_digit_tpl_map[key] += ones_digit
        
        part1 += secret

    part2 = max(ones_digit_tpl_map.values())
    print(part1, part2)


if __name__ == '__main__':
    main()

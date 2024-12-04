import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def card_config(line: str):
    winning, all = line.split(' | ')
    winning_cards = [int(w) for w in winning.split()[2:]]
    all_cards = [int(w) for w in all.split()]
    card_no = int(winning.split()[1][:-1])
    return (card_no - 1, winning_cards, all_cards)


def main():
    input_lines = sys.stdin.read().split('\n')
    cards = [card_config(line) for line in input_lines]

    # parts 1 and 2
    ret, copies = 0, [1] * len(cards)
    for card_no, winning, all in cards:
        matches = len(set(winning) & set(all))
        if matches > 0:
            ret += 2 ** (matches - 1)
        for i in range(matches):
            copies[i + 1 + card_no] += copies[card_no]

    print(ret, sum(copies))


if __name__ == '__main__':
    main()
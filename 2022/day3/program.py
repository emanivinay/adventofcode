import sys
from string import ascii_letters

# Reads input from stdin - on a terminal, run this like
# cat input.txt | python3 program.py

def priority(item):
    return ascii_letters.index(item) + 1


def unique_common_item(*bags):
    return [letter for letter in ascii_letters 
        if all(letter in bag for bag in bags)][0]


def solve1(rucksacks):
    ret = 0
    for rucksack in rucksacks:
        N = len(rucksack)
        comp1, comp2 = rucksack[:N // 2], rucksack[N // 2:]
        ret += priority(unique_common_item(comp1, comp2))
    return ret


def solve2(rucksacks):
    ret = 0
    N = len(rucksacks)
    for i in range(N // 3):
        ret += priority(unique_common_item(*rucksacks[3 * i : 3 * i + 3]))
    return ret


def main():
    rucksacks = [line.strip() for line in sys.stdin.readlines()]
    print(solve1(rucksacks))
    print(solve2(rucksacks))


if __name__ == '__main__':
    main()
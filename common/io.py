import sys


def read_numbers(sep=' ', converter=int):
    return [[converter(word) for word in line.split(sep)] for line in sys.stdin.readlines()]
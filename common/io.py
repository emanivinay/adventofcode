import sys


def read_and_convert_all_lines(sep=' ', converter=int):
    return [[converter(word) for word in line.split(sep)] for line in sys.stdin.readlines()]


def read_and_convert_one_line(sep=' ', converter=int):
    return [converter(token) for token in sys.stdin.readline().split(sep)]

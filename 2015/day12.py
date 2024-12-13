import sys
import collections
import itertools
import functools
import json


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def sum_recursive(data):
    if data is None:
        return 0
    if isinstance(data, int):
        return data
    if isinstance(data, list):
        return sum(sum_recursive(elem) for elem in data)
    elif isinstance(data, dict):
        if "red" in data.values():
            return 0
        return sum(sum_recursive(elem) for elem in data.values())
    else:
        return 0


def main():
    data = json.loads(sys.stdin.read())
    print(sum_recursive(data))


if __name__ == '__main__':
    main()

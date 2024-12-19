import sys
import collections
import itertools
import functools
import re


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def parse_tree_from_numbers(numbers):
    def read_node_from(index):
        num_children, num_metadata_entries = numbers[index : index + 2]
        index += 2
        children = []
        for _ in range(num_children):
            index, child = read_node_from(index)
            children.append(child)

        metadata = numbers[index : index + num_metadata_entries]
        index += num_metadata_entries
        return index, (children, metadata)

    return read_node_from(0)


def main():
    numbers = [int(w) for w in re.split(r'[ \n]+', sys.stdin.read())]
    _, root = parse_tree_from_numbers(numbers)

    def recurse(node, visitor):
        visitor(node)
        for child in node[0]:
            recurse(child, visitor)
    
    metadata_total = 0
    def sum_metadata_entries(node):
        nonlocal metadata_total
        metadata_total += sum(node[1])
    
    recurse(root, sum_metadata_entries)
    print(metadata_total)

    def value(node):
        children, metadata = node
        num_children = len(children)
        if num_children == 0:
            return sum(metadata)
        ret = 0
        children_values = [value(c) for c in children]
        for m in metadata:
            if 1 <= m <= num_children:
                ret += children_values[m - 1]
        return ret
    
    print(value(root))


if __name__ == '__main__':
    main()

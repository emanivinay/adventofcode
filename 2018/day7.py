import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    dependencies = collections.defaultdict(list)
    depended_by = collections.defaultdict(list)
    all_tasks = set()
    for line in sys.stdin.read().split('\n'):
        tokens = line.split()
        a, b = tokens[1], tokens[7]
        all_tasks.add(a)
        all_tasks.add(b)
        dependencies[b].append(a)
        depended_by[a].append(b)

    all_tasks = sorted(all_tasks)
    order = []
    while True:
        next_task = None
        for task in all_tasks:
            if task in order:
                continue
            deps = dependencies[task]
            if not deps and (next_task is None or next_task > task):
                next_task = task
        if next_task is None:
            break
        order.append(next_task)
        for dependant in depended_by[next_task]:
            dependencies[dependant].remove(next_task)

    print(''.join(order))


if __name__ == '__main__':
    main()

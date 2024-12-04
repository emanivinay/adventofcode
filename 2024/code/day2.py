import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def is_report_safe(report):
    assert len(report) >= 2
    if report[0] == report[1]:
        return False
    order = report[0] > report[1]
    for i in range(1, len(report)):
        delta = abs(report[i - 1] - report[i])
        if delta < 1 or delta > 3:
            return False
        if (report[i - 1] > report[i]) != order:
            return False
    return True


def is_report_safe_after_dampening(report):
    if is_report_safe(report):
        return True
    n = len(report)
    for i in range(n):
        report2 = report[:i] + report[i + 1:]
        if is_report_safe(report2):
            return True
    return False


def main():
    input_lines = sys.stdin.read().split('\n')
    reports = [split_ints(line) for line in input_lines]
    num_safe_reports, num_safe_after_dampening = 0, 0
    for report in reports:
        if is_report_safe(report):
            num_safe_reports += 1
        if is_report_safe_after_dampening(report):
            num_safe_after_dampening += 1

    print("Part 1", num_safe_reports)
    print("Part 2", num_safe_after_dampening)


if __name__ == '__main__':
    main()
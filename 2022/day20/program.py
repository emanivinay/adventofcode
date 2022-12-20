import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def get_remainder(x, N):
    if x >= 0:
        return x % N
    
    return (N - (-x) % N) % N


def mix(numbers, dec_key=1):
    N = len(numbers)

    for iter in range(N):
        pos, val = 0, 0
        for i in range(N):
            if iter == numbers[i][0]:
                pos = i
                val = numbers[i][1]
                break
        
        removed = numbers.pop(pos)
        if pos > 0:
            new_pos = pos - 1
        else:
            new_pos = N - 2
        
        new_pos += get_remainder(val, N - 1)
        new_pos %= N - 1
        numbers.insert((new_pos + 1) % (N - 1), removed)
    
    return numbers


def sum_3(numbers):
    zero_pos = -1
    for i in range(len(numbers)):
        if numbers[i][1] == 0:
            zero_pos = i

    ret, pos = 0, zero_pos
    for i in range(3):
        pos += 1000
        add = numbers[pos % len(numbers)][1]
        ret += add
    return ret


def main():
    input_lines = sys.stdin.read().split('\n')
    numbers = [(i, int(line)) for i, line in enumerate(input_lines)]
    originals = numbers[:]
    # part 1
    print(sum_3(mix(numbers)))

    # part 2
    DEC_KEY = 811589153
    numbers = [(i, v * DEC_KEY) for (i, v) in originals]

    for _ in range(10):
        numbers = mix(numbers)
    
    print(sum_3(numbers))


if __name__ == '__main__':
    main()
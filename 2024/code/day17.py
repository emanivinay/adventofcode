import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def machine(register_set, program):
    output = []

    def operand_value(operand, is_combo):
        if not is_combo or operand <= 3:
            return operand
        reg = "ABC"[operand - 4]
        return register_set[reg]
    
    iptr = 0
    while 0 <= iptr < len(program):
        opcode, operand = program[iptr], program[iptr + 1]
        is_combo = opcode in (0, 2, 5, 6, 7)
        op_val = operand_value(operand, is_combo)
        if opcode in (0, 6, 7):
            dest_register = 'A' if opcode == 0 else ('B' if opcode == 6 else 'C')
            register_set[dest_register] = register_set['A'] >> op_val
        elif opcode == 1:
            register_set['B'] ^= op_val
        elif opcode == 2:
            register_set['B'] = op_val % 8
        elif opcode == 3:
            if register_set['A'] != 0:
                iptr = op_val - 2
        elif opcode == 4:
            register_set['B'] ^= register_set['C']
        else:
            output.append(op_val % 8)
        iptr += 2

    return output


BITS = 64


def xor_simplify(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a ^ b
    elif a == 0:
        return b
    else:
        return ('xor', 1, b)


def bits(n):
    return n % 2, n // 2 % 2, n // 4 % 2


def final_value(A_mapping):
    ret = 0
    for i in range(BITS):
        cur = A_mapping[i]
        if not isinstance(cur, int):
            cur = 0
        ret += cur << i
    return ret


def check(i, A_mapping, b):
    cur = A_mapping[i]
    if isinstance(cur, int) and cur != b:
        return False
    return True


def try_and_match(B, ts, A_mapping):
    ret = dict()
    for b, t in zip(B, ts):
        if isinstance(b, int):
            if b != t:
                return None
        elif isinstance(b, str):
            i = int(b[1:])
            if not check(i, A_mapping, t):
                return None
            ret[i] = t
        else:
            _, _, v = b
            t2 = t ^ 1
            # match v with t2
            i = int(v[1:])
            if not check(i, A_mapping, t2):
                return None
            ret[i] = t2
    return ret

# Program is 2,4 1,3 7,5 1,5 0,3 4,1 5,5 3,0
# Repeat 16 times
#   B = A % 8
#   B = B ^ 3
#   C = A >> B
#   B = B ^ 5
#   A = A >> 3
#   B = B ^ C % 8
#   output(B)


def print_mappings(A_mapping):
    for k, v in A_mapping.items():
        if isinstance(v, int):
            print(k, v, sep='-', end=',')
    print()


def recurse(index, program, A_mapping):
    if index == len(program):
        print(final_value(A_mapping))
        return

    offset = 3 * index
    target_bits = bits(program[index])

    for mask in range(8):
        bits3 = [b0, b1, b2] = bits(mask)
        if any(not check(offset + j, A_mapping, bits3[j]) for j in range(3)):
            continue

        A_mapping_new = dict(A_mapping)
        for j in range(3):
            A_mapping_new[offset + j] = bits3[j]

        B = [b0 ^ 1, b1 ^ 1, b2]
        B_offset = B[0] + B[1] * 2 + B[2] * 4
        C = [A_mapping_new[offset + B_offset + j] for j in range(3)]
        B = [B[0] ^ 1, B[1], B[2] ^ 1]

        output = [xor_simplify(b, c) for b, c in zip(B, C)]
        new_mappings = try_and_match(output, target_bits, A_mapping_new)
        if new_mappings is not None:
            A_mapping_new.update(new_mappings)
            recurse(index + 1, program, A_mapping_new)


def main():
    register_set = dict(A=21539243, B=0, C=0)
    program = [2,4, 1,3, 7,5, 1,5, 0,3, 4,1, 5,5, 3,0]
    print(*machine(register_set, program), sep=',')

    A_mapping = dict((i, f'A{i}') for i in range(BITS))
    recurse(0, program, A_mapping)


if __name__ == '__main__':
    main()

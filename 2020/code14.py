import sys
import collections
import itertools
import functools


def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def main():
    # (2^36) - 1
    ALL_BITS_MASK = 0xFFFFFFFFF

    mask_and_by, mask_or_by = 0, 0
    mask = ''
    registers = collections.defaultdict(int)

    def parse_mask_str(mask_str):
        mask_and_by = mask_or_by = 0
        _, mask_str = line.split(' = ')   
        for i, b in enumerate(mask_str[::-1]):
            if b == '0':
                mask_and_by |= 1 << i
            elif b == '1':
                mask_or_by |= 1 << i
        return mask_and_by, mask_or_by

    
    def get_address_range_after_masking(address, mask):
        ret = ['X'] * 36
        for i in range(36):
            bit = 35 - i
            if mask[bit] == '1':
                ret[bit] = '1'
            elif mask[bit] == '0':
                ret[bit] = '1' if (address & (1 << bit)) else '0'
        return ''.join(ret)

    for line in sys.stdin.read().split('\n'):
        if line.startswith('mask'):
            mask = line.split(' = ')[1]
            mask_and_by, mask_or_by = parse_mask_str(mask)
        else:
            dest, val = line.split(' = ')
            val = int(val)
            dest = int(dest[4:-1])
            registers[dest] = (val & ~mask_and_by) | mask_or_by
    
    part1 = sum(registers.values())
    print(part1)


if __name__ == '__main__':
    main()

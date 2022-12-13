import sys


# Parse input lines with the starting stack configuration
def parse_stack_lines(stack_lines):
    N = 9
    stacks = [[] for _ in range(N)]
    for line in stack_lines:
        for i in range(N):
            crate = line[4 * i : 4 * i + 3]
            if crate.strip():
                stacks[i].append(crate[1])
    
    # Top items at the back so append and pop work efficiently.
    return [stack[::-1] for stack in stacks]


# Given source to destination stack crate move order, simulate CrateMover
def solve(stacks, move_lines, crate_mover_func):
    for line in move_lines:
        words = line.split()
        count, src_stack, dst_stack = int(words[1]), int(words[3]) - 1, int(words[5]) - 1
        crate_mover_func(stacks[src_stack], stacks[dst_stack], count)
    
    print(''.join(stack[-1] for stack in stacks))


# Removes count stacks from src and places them on dst in reverse order
def reverse_order_mover(src, dst, count):
    for _ in range(count):
        dst.append(src.pop())


# Removes count stacks from src and places them on dst in the same order
# Same order swap can be simulated with two reverse order swaps using a temporary middle stack
def same_order_mover(src, dst, count):
    temp_stack = []
    reverse_order_mover(src, temp_stack, count)
    reverse_order_mover(temp_stack, dst, count)


def main():
    input_lines = [line for line in sys.stdin.readlines()]
    stacks = parse_stack_lines(input_lines[:8])
    stacks_copy = [stack[:] for stack in stacks]
    move_lines = input_lines[10:]
    
    solve(stacks, move_lines, reverse_order_mover)
    solve(stacks_copy, move_lines, same_order_mover)


if __name__ == '__main__':
    main()
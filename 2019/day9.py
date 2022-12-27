from intcode import simulate_intcode_computer


MAX_PROGRAM_MEMORY = 1 << 20


def main():
    program = [int(x) for x in open('input9.txt').read().split(',')]
    extra_memory_needed = MAX_PROGRAM_MEMORY - len(program)
    program += [0] * extra_memory_needed
    simulate_intcode_computer(program)


main()
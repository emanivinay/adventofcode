from intcode import simulate_intcode_computer


def main():
    xx = open('input5.txt').read()
    program = [int(x) for x in xx.split(',')]
    simulate_intcode_computer(program)


main()
import functools

@functools.lru_cache
def comparer(operator):
    match operator.strip():
        case '>':
            return lambda x, y: x > y
        case '<':
            return lambda x, y: x < y
        case '>=':
            return lambda x, y: x >= y
        case '<=':
            return lambda x, y: x <= y
        case '==':
            return lambda x, y: x == y
        case _:
            return lambda x, y: x != y


def parse_instruction_line(line):
    register, idec, change, _, input_reg, operation, constant = line.split()
    change = int(change)
    constant = int(constant)
    if idec == 'dec':
        change = -change
    
    return (register, change, input_reg, comparer(operation), constant)
    

def main():
    # Run the instructions
    register_values = dict()
    best = 0
    for line in open('input8.txt').readlines():
        register, change, input_reg, comparer, const = parse_instruction_line(line)
        if comparer(register_values.get(input_reg, 0), const):
            value = register_values[register] = register_values.get(register, 0) + change
            best = max(best, value)
    
    # parts 1 and 2
    print(max(register_values.values()), best)


main()
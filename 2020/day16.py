import sys


def parse_input_lines(input_lines):
    fields = []
    field_names = []

    def parse_range_str(s):
        return tuple(int(x) for x in s.split('-'))

    your_ticket, other_tickets = None, []
    for line in input_lines:
        if 'or' in line:
            tokens = line.split()
            r1, r2 = tokens[-3], tokens[-1]
            fields.append((parse_range_str(r1), parse_range_str(r2)))
            field_name = line.split(':')[0]
            field_names.append(field_name)
        elif line and line[0].isdigit():
            numbers = list(int(x) for x in line.split(','))
            if your_ticket is None:
                your_ticket = numbers
            else:
                other_tickets.append(numbers)
    
    return (fields, field_names, your_ticket, other_tickets)


def is_number_within_range(number, range):
    a, b = range
    return a <= number <= b

def does_field_match_position_in_all_tickets(field, tickets, pos):
    for ticket in tickets:
        number = ticket[pos]
        if all(not is_number_within_range(number, range) for range in field):
            return False
    
    return True


def main():
    input_lines = [line.strip() for line in sys.stdin.readlines()]
    fields, field_names, mine, others = parse_input_lines(input_lines)

    # part 1
    scan_error_rate = 0
    valid_tickets = [mine]
    for ticket in others:
        valid = True
        for number in ticket:
            no_matching_field = True
            for field in fields:
                if any(is_number_within_range(number, range) for range in field):
                    no_matching_field = False
                    break
            
            if no_matching_field:
                valid = False
                scan_error_rate += number
        
        if valid:
            valid_tickets.append(ticket)
    
    print(scan_error_rate)

    # part 2 - simple iterative elimination of invalid field <-> ticket matches
    n_fields = len(fields)
    n_cols = len(valid_tickets[0])
    field_pos_match_matrix = [[False] * n_cols for _ in range(n_fields)]
    for i in range(n_fields):
        for pos in range(n_cols):
            if does_field_match_position_in_all_tickets(fields[i], valid_tickets, pos):
                field_pos_match_matrix[i][pos] = True
    
    matched_fields_set = set()
    for _ in range(n_fields):
        for f in range(n_fields):
            if f in matched_fields_set:
                continue
            matching_cols = [j for j in range(n_cols) if field_pos_match_matrix[f][j]]
            if len(matching_cols) == 1:
                matched_fields_set.add(f)
                col = matching_cols[0]
                for f2 in range(n_fields):
                    field_pos_match_matrix[f2][col] = (f2 == f)
                break
    
    ret = 1
    for f in range(n_fields):
        if not field_names[f].startswith('departure'):
            continue
        for i in range(n_cols):
            if field_pos_match_matrix[f][i]:
                ret *= mine[i]
    
    print(ret)


main()
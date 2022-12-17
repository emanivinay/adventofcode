import sys


def parse_aunt_input_line(line):
    tokens = line.split()
    aunt_no = int(tokens[1][:-1])
    items = ' '.join(tokens[2:]).split(', ')
    bag = dict()
    for item in items:
        item_name, count = item.split(': ')
        bag[item_name] = int(count)
    
    return {
        'id': aunt_no,
        'items': bag,
    }


DETECTED = {
    'children': 3,
    'cats': 7, # > 7
    'samoyeds': 2,
    'pomeranians': 3, # < 3
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5, # < 5
    'trees': 3, # > 3
    'cars': 2,
    'perfumes': 1,
}

def check_item_count(item_name, count_in_set, detected_count):
    if item_name in ('cats', 'trees'):
        return count_in_set > detected_count
    elif item_name in ('goldfish', 'pomeranians'):
        return count_in_set < detected_count
    else:
        return count_in_set == detected_count



def is_itemset_compatible(item_set, detected, question_part):
    for item_name, count in detected.items():
        if item_name not in item_set:
            continue
        if question_part == 1 and count != item_set[item_name]:
            return False
        if question_part == 2 and not check_item_count(item_name, item_set[item_name], count):
            return False
    
    return True


def main():
    aunts = [parse_aunt_input_line(line) for line in sys.stdin.readlines()]
    for aunt in aunts:
        if is_itemset_compatible(aunt['items'], DETECTED, 1):
            print(aunt)
        if is_itemset_compatible(aunt['items'], DETECTED, 2):
            print(aunt)

main()
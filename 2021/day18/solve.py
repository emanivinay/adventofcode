import sys


def max_depth(node):
    if isinstance(node, int):
        return 0
    return 1 + max(max_depth(node[0]), max_depth(node[1]))


def max_regular_number(node):
    if isinstance(node, int):
        return node
    return max(max_regular_number(node[0]), max_regular_number(node[1]))


def get_parent_of_right_most_regular_no(lst, estack, i):
    if isinstance(lst, int):
        return estack[i - 1]

    ret = lst
    while isinstance(lst, list):
        ret = lst
        lst = lst[1]
    return ret


def get_parent_of_left_most_regular_no(lst, estack, i):
    if isinstance(lst, int):
        return estack[i - 1]

    ret = lst
    while isinstance(lst, list):
        ret = lst
        lst = lst[0]
    return ret


def is_regular_pair(node):
    return isinstance(node, list) and isinstance(node[0], int) and isinstance(node[1], int)


def get_exploding_pair(lst):
    node, stack, direction = lst, [], None
    while len(stack) < 4:
        need_depth = 4 - len(stack)
        stack.append((node, direction))
        if max_depth(node[0]) >= need_depth:
            # going left
            node = node[0]
            direction = 0
        elif max_depth(node[1]) >= need_depth:
            # going right
            node = node[1]
            direction = 1
        else:
            return (None, None)
    
    while not is_regular_pair(node):
        stack.append((node, direction))
        if isinstance(node[0], list):
            direction = 0
            node = node[0]
        else:
            direction = 1
            node = node[1]
    
    stack.append((node, direction))
    return (stack, node)


def get_splitting_number(lst):
    node, parent, direction = lst, None, None
    if max_regular_number(node) < 10:
        return (None, None)
    
    while isinstance(node, list):
        parent = node
        if max_regular_number(node[0]) >= 10:
            node = node[0]
            direction = 0
        else:
            node = node[1]
            direction = 1
    
    return (parent, direction)
    

def reduce(number):
    estack, enode = get_exploding_pair(number)
    if enode is None:
        # no exploding pair, look for splitting number
        spar, sdir = get_splitting_number(number)
        if sdir is None:
            return
        snumber = spar[sdir]
        a = snumber // 2
        b = (snumber + 1) // 2
        spar[sdir] = [a, b]
    else:
        # There is an exploding pair.
        [a, b] = enode
        n = len(estack)
        for i in range(n - 1, 0, -1):
            if estack[i][1] == 1:
                sibling = estack[i - 1][0]
                to_add = get_parent_of_right_most_regular_no(sibling, estack, i - 1)
                to_add[1] += a
        
        for i in range(n - 1, 0, -1):
            if estack[i][1] == 0:
                sibling = estack[i - 1][1]
                to_add = get_parent_of_left_most_regular_no(sibling, estack, i - 1)
                to_add[0] += b

        estack[-2][estack[-1][1]] = 0


def add_snailfish_numbers(number1, number2):
    new_number = [number1, number2]
    reduce(new_number)
    return new_number


def magnitude(number):
    if isinstance(number, int):
        return number
    
    a, b = number
    return 3 * magnitude(a) + 2 * magnitude(b)


def main():
    numbers = [eval(line.strip()) for line in sys.stdin.readlines()]

    # part 1
    result = None
    for number in numbers[:2]:
        if result is None:
            result = number
        else:
            result = add_snailfish_numbers(result, number)
    print(magnitude(result))


main()
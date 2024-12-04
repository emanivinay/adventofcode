import sys


def perm_to_str(perm):
    return ''.join(chr(ord('a') + c) for c in perm)


def perform_dance(perm, moves):
    for move in moves:
        if move[0] == 's':
            X = int(move[1:])
            perm = perm[-X:] + perm[:-X]
        elif move[0] == 'x':
            a, b = move[1:].split('/')
            a = int(a)
            b = int(b)
            perm[a], perm[b] = perm[b], perm[a]
        else:
            a, b = move[1:].split('/')
            a = perm.index(ord(a) - 97)
            b = perm.index(ord(b) - 97)
            perm[a], perm[b] = perm[b], perm[a]
    
    return perm


def main():
    moves = sys.stdin.read().strip().split(',')
    perm = perform_dance(list(range(16)), moves)

    # part 1
    print(perm_to_str(perm))

    # part 2
    i = 0
    perm = list(range(16))
    perm0 = perm[:]

    while True:
        perm = perform_dance(perm, moves)
        i += 1
        if perm == perm0:
            break

    # For this cycle, offset is zero.
    cycle = i
    rem = 1000000000 % cycle
    for _ in range(rem):
        perm = perform_dance(perm, moves)
    
    print(perm_to_str(perm))


main()
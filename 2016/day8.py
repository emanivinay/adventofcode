import sys


WIDTH, HEIGHT = 50, 6


def parse_instr_line(instr):
    tokens = instr.split()
    if tokens[0] == 'rect':
        A, B = tokens[1].split('x')
        return ('rect', int(A), int(B))
    
    # rotate row/col x/y=A by B
    A = int(tokens[2].split('=')[1])
    B = int(tokens[4])
    return ('rotate', tokens[1], A, B)


def main():
    instrs = [line.strip() for line in sys.stdin.readlines()]
    grid = [[0] * WIDTH for _ in range(HEIGHT)]
    for instr in instrs:
        *tokens, A, B = parse_instr_line(instr)
        if tokens[0] == 'rect':
            for b in range(B):
                for a in range(A):
                    grid[b][a] = 1
        elif tokens[1] == 'row':
            B = B % WIDTH
            if B > 0:
                grid[A] = grid[A][-B:] + grid[A][:-B]
        else:
            B = B % HEIGHT
            if B > 0:
                col = [grid[y][A] for y in range(HEIGHT)]
                col_shifted = col[-B:] + col[:-B]
                for y in range(HEIGHT):
                    grid[y][A] = col_shifted[y]
    
    # part 1
    print(sum(row.count(1) for row in grid))

    # part 2
    for row in grid:
        print(''.join('*' if x == 1 else ' ' for x in row))


if __name__ == '__main__':
    main()
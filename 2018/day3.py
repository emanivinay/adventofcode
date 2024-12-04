import sys


def parse_claim_line(line):
    eid, dims = line.split(' @ ')
    eid = int(eid[1:])
    top_left, dims = dims.split(': ')
    tx, ty = [int(w) for w in top_left.split(',')]
    lx, ly = [int(w) for w in dims.split('x')]
    return (eid, (tx, ty), (lx, ly))


def main():
    MAX = 1024
    grid = [[0] * MAX for _ in range(MAX)]
    claims = [parse_claim_line(l.strip()) for l in sys.stdin.readlines()]

    for claim in claims:
        _, (tx, ty), (lx, ly) = claim
        for x in range(tx, tx + lx):
            for y in range(ty, ty + ly):
                grid[x][y] += 1
    
    # part 1
    print(sum(cell >= 2 for row in grid for cell in row))

    # part 2
    for claim in claims:
        eid, (tx, ty), (lx, ly) = claim
        if all(grid[x][y] == 1 for x in range(tx, tx + lx) for y in range(ty, ty + ly)):
            print(eid)
            break


if __name__ == '__main__':
    main()
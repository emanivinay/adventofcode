import sys

DIRECTIONS = [(0, -1), (-1, 0), (0, 1), (1, 0)]

def dimensions(grid):
    return (len(grid), 0 if not grid else len(grid[0]))


def tree_seq_to_edge(grid, R, C, r, c, dir):
    dy, dx = dir
    while True:
        r, c = r + dy, c + dx
        if 0 <= r < R and 0 <= c < C:
            yield grid[r][c]
        else:
            break


def count_visible(grid):
    R, C = dimensions(grid)
    ret = 0
    for r in range(R):
        for c in range(C):
            visible = False
            for dir in DIRECTIONS:
                if all(tree < grid[r][c] for tree in tree_seq_to_edge(grid, R, C, r, c, dir)):
                    visible = True
            ret += visible
    
    return ret


def get_scenic_score(grid, R, C, r, c):
    ret = 1
    for dir in DIRECTIONS:
        seen = 0
        for ht in tree_seq_to_edge(grid, R, C, r, c, dir):
            seen += 1
            if ht >= grid[r][c]:
                break
        ret *= seen

    return ret


def best_scenic_score(grid):
    R, C = dimensions(grid)
    ret = 0
    for r in range(R):
        for c in range(C):
            ret = max(ret, get_scenic_score(grid, R, C, r, c))
    return ret


def main():
    grid = sys.stdin.read().split('\n')

    # part 1
    print(count_visible(grid))

    # part 2
    print(best_scenic_score(grid))


if __name__ == '__main__':
    main()
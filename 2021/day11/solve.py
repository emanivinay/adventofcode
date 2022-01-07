def simulate(grid):
    flashed = [[False] * 10 for _ in range(10)]

    def add(y, x):
        grid[y][x] += 1
        if not flashed[y][x] and grid[y][x] > 9:
            flashed[y][x] = True
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dy != 0 or dx != 0:
                        y2, x2 = y + dy, x + dx
                        if y2 in range(10) and x2 in range(10):
                            add(y2, x2)


    for i in range(10):
        for j in range(10):
            add(i, j)

    ret = 0
    for i in range(10):
        for j in range(10):
            if flashed[i][j]:
                grid[i][j] = 0
                ret += 1

    return ret


def main():
    grid = [[int(w) for w in input().strip()] for _ in range(10)]
    step = 1
    while simulate(grid) != 100:
        step += 1
    print(step)


main()

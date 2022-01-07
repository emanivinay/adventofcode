import sys
import heapq

def readInputData():
    return [[int(w) for w in input().strip()] for _ in range(100)]


def repeatGrid(grid, x):
    H = len(grid)
    W = len(grid[0])

    ret = [[0] * (W * x) for _ in range(H * x)]
    for i in range(H * x):
        for j in range(W * x):
            ret[i][j] = grid[i % H][j % W] + i // H + j // W
            while ret[i][j] > 9:
                ret[i][j] -= 9

    return ret


def main():
    grid = readInputData()
    REP = int(sys.argv[1])
    grid = repeatGrid(grid, REP)
    W = len(grid[0])
    H = len(grid)

    BIG = 1 << 40
    queue = []
    distance = [[BIG] * W for _ in range(H)]

    def add(y, x, cost):
        if 0 <= y < H and 0 <= x < W and distance[y][x] > cost + grid[y][x]:
            distance[y][x] = cost + grid[y][x]
            heapq.heappush(queue, (distance[y][x], y, x))

    add(0, 0, -grid[0][0])

    while queue:
        cost, y, x = queue[0]
        heapq.heappop(queue)
        add(y + 1, x, cost)
        add(y - 1, x, cost)
        add(y, x + 1, cost)
        add(y, x - 1, cost)

    print(distance[H - 1][W - 1])


if __name__ == '__main__':
    main()

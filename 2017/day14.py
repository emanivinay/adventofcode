from day10 import knot_hash, get_dense_hash
from collections import deque

def main():
    puzzle_key = 'nbysizxe'
    N = 256
    D = 128

    grid = []
    for r in range(D):
        knot_hash_lengths = [ord(c) for c in f'{puzzle_key}-{r}'] + [17, 31, 73, 47, 23]
        sparse_hash = knot_hash(256, knot_hash_lengths, 64)
        dense_hash = get_dense_hash(sparse_hash, N) # 16 bytes
        grid.append(''.join(bin(byte)[2:].rjust(8, '0') for byte in dense_hash))

    # part 1
    print(sum(row.count('1') for row in grid))

    # part 2
    visited = [[False] * D for _ in range(D)]
    groups = 0

    def visit(y, x, queue):
        if y < 0 or x < 0 or max(y, x) >= D or visited[y][x] or grid[y][x] != '1':
            return
        queue.append((y, x))
        visited[y][x] = True

    for i in range(D):
        for j in range(D):
            if grid[i][j] == '1' and not visited[i][j]:
                groups += 1
                queue = deque()
                visit(i, j, queue)

                while queue:
                    y, x = queue.popleft()
                    visit(y, x + 1, queue)
                    visit(y, x - 1, queue)
                    visit(y + 1, x, queue)
                    visit(y - 1, x, queue)
    
    print(groups)


if __name__ == '__main__':
    main()
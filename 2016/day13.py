from collections import deque, defaultdict


FAVORITE_NO = 1350


def bit_count(x, y, favorite):
    v = x * x + 3 * x + 2 * x * y + y + y * y + favorite
    return bin(v).count('1') % 2


def bfs():
    queue = deque()
    distance = defaultdict(lambda: -1)

    def push(x, y, d):
        if min(x, y) >= 0 and distance[(x, y)] < 0 and bit_count(x, y, FAVORITE_NO) == 0:
            distance[(x, y)] = d
            queue.append((x, y))

    push(1, 1, 0)

    while queue:
        x, y = queue.popleft()
        d = distance[(x, y)]
        if d >= 50:
            break
        push(x + 1, y, d + 1)
        push(x - 1, y, d + 1)
        push(x, y + 1, d + 1)
        push(x, y - 1, d + 1)

    return sum(d >= 0 for d in distance.values())


def main():
    print(bfs())


main()

import sys
from collections import deque


def flip(cur, bit):
    y, x = bit // 5, bit % 5
    nxt = cur ^ (1 << bit)
    if y >= 1:
        nxt = nxt ^ (1 << (bit - 5))
    if y < 4:
        nxt = nxt ^ (1 << (bit + 5))
    if x >= 1:
        nxt = nxt ^ (1 << (bit - 1))
    if x < 4:
        nxt = nxt ^ (1 << (bit + 1))
    
    return nxt


distance = [-1] * (1 << 25)
pred = [None] * (1 << 25)


def main():
    start = (1 << 7) + (1 << 22)
    queue = deque()
    queue.append(start)
    distance[start] = 0
    prev_dist = -1
    while queue:
        cur = queue.popleft()
        dst = distance[cur]
        if prev_dist >= 0 and dst > prev_dist:
            print(dst)
        prev_dist = dst

        if cur == 0:
            print('solution found')
            break
        dst = distance[cur]
        for y in range(5):
            for x in range(5):
                bit = 5 * y + x
                nxt = flip(cur, bit)
                if distance[nxt] < 0:
                    distance[nxt] = 1 + dst
                    pred[nxt] = bit
                    queue.append(nxt)
    
    cur = 0
    while cur != start:
        bit = pred[cur]
        print(bit // 5, bit % 5)
        cur = flip(cur, bit)


if __name__ == '__main__':
    main()
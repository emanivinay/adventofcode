import sys

def processInput():
    data = [l.strip() for l in sys.stdin.readlines()]
    lines = []
    for d in data:
        tokens = d.split()
        x1, y1 = tokens[0].split(',')
        x2, y2 = tokens[2].split(',')
        lines.append((x1, y1, x2, y2))
        lines[-1] = [int(w) for w in lines[-1]]

    return lines

def iterdir(a, b):
    diff = 1 if a < b else -1
    yield from range(a, b + diff, diff)


def main():
    lines = processInput()
    cover = [[0] * 1000 for _ in range(1000)]
    for x1, y1, x2, y2 in lines:
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                cover[x1][y] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                cover[x][y1] += 1
        elif x1 + y1 == x2 + y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                y = x1 + y1 - x
                cover[x][y] += 1
        elif x1 - y1 == x2 - y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                y = x - x1 + y1
                cover[x][y] += 1

    dangerous = 0
    for y in range(1000):
        for x in range(1000):
            if cover[x][y] > 1:
                dangerous += 1

    print(dangerous)

main()

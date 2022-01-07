import sys


def main():
    MAX = 26
    ITERS = int(sys.argv[1])

    def code(c):
        return ord(c) - ord('A')
    
    polymer = input().strip()

    input()

    rules = dict()
    for _ in range(100):
        line = input().strip()
        a, b = line.split(' -> ')
        rules[(code(a[0]), code(a[1]))] = code(b)

    pairs = [[0] * MAX for _ in range(MAX)]
    for i in range(1, len(polymer)):
        a, b = polymer[i - 1], polymer[i]
        pairs[code(a)][code(b)] += 1

    last = code(polymer[-1])

    for _ in range(ITERS):
        newPairs = [[0] * MAX for _ in range(MAX)]
        for i in range(MAX):
            for j in range(MAX):
                if (i, j) in rules:
                    k = rules[(i, j)]
                    newPairs[i][k] += pairs[i][j]
                    newPairs[k][j] += pairs[i][j]
                else:
                    newPairs[i][j] = pairs[i][j]

        pairs = newPairs

    counter = [0] * MAX
    for i in range(MAX):
        for j in range(MAX):
            counter[i] += pairs[i][j]
        if i == last:
            counter[i] += 1

    print(max(counter) - min(c for c in counter if c > 0))

main()

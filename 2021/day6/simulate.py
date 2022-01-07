from functools import lru_cache


def simulate(school, days):
    counter = [0] * 10
    for f in school:
        counter[f] += 1

    for _ in range(days):
        newCounter = [0] * 10
        newCounter[8] = counter[0]
        newCounter[6] = counter[0]

        for i in range(1, 9):
            newCounter[i - 1] += counter[i]

        counter = newCounter

    print(sum(counter))


@lru_cache(maxsize=None)
def f(i, days):
    if days == 0:
        return 1

    if i == 0:
        return f(6, days - 1) + f(8, days - 1)

    return f(i - 1, days - 1)


def main():
    data = list(int(w) for w in open('input.txt').readlines()[0].split(','))
    print(sum(f(i, 256) for i in data))
    simulate(data, 256)


if __name__ == '__main__':
    main()

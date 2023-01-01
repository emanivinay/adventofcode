from math import lcm


def simulate(delay, radars):
    for i, r in radars:
        t = i + delay
        if t % (2 * (r - 1)) == 0:
            return False

    return True


def main():
    radars = [line.strip().split(': ') for line in open('input13.txt').readlines()]
    radars = [(int(x), int(y)) for (x, y) in radars]

    delay = 0
    while not simulate(delay, radars):
        delay += 1
    print(delay)


if __name__ == '__main__':
    main()
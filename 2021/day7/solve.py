def processInput():
    line = open('input.txt').readlines()[0]
    return [int(word) for word in line.split(',')]


def moveCostForAllCrabs(x, crabs, moveCostSingleCrab):
    return sum(moveCostSingleCrab(x - pos) for pos in crabs)


def leastMovingCost(crabs, moveCostSingleCrab):
    lo, hi = min(crabs), max(crabs)
    while hi - lo > 2:
        mid1 = (lo * 2 + hi) // 3
        mid2 = (lo + hi * 2) // 3
        cost1 = moveCostForAllCrabs(mid1, crabs, moveCostSingleCrab)
        cost2 = moveCostForAllCrabs(mid2, crabs, moveCostSingleCrab)

        if cost1 < cost2:
            hi = mid2
        else:
            lo = mid1

    return min(moveCostForAllCrabs(x, crabs, moveCostSingleCrab) for x in range(lo, hi + 1))


def main():
    crabs = sorted(processInput())
    # puzzle 1
    print(leastMovingCost(crabs, lambda x:abs(x)))

    # puzzle 2
    print(leastMovingCost(crabs, lambda x:abs(x) * (abs(x) + 1) // 2))


main()

def processInput(inputFile='input.txt'):
    return [l.strip() for l in open(inputFile).readlines()]


def filter(data, a=1):
    setA = set(range(len(data)))
    setB = set(range(len(data)))

    def count(bit, value, dataset):
        return set(d for d in dataset if data[d][bit] == value)

    for bit in range(12):
        onesA = count(bit, '1', setA)
        zerosA = count(bit, '0', setA)

        onesB = count(bit, '1', setB)
        zerosB = count(bit, '0', setB)

        setA = onesA if len(onesA) >= len(zerosA) else zerosA
        setB = onesB if len(onesB) < len(zerosB) else zerosB

        if not setB:
            setB = onesB or zerosB

    x, y = data[min(setA)], data[min(setB)]
    print(int(x, 2) * int(y, 2))


filter(processInput())

from itertools import permutations


def readInputData():
    data = []
    for line in open('input.txt').readlines():
        words = line.split()
        words.pop(10)
        data.append(words)

    return data


def decodeSingle(digit, new_list, originals):
    pass


def decode(entry):
    # 2 - cf
    # 3 - acf
    # 4 - bcdf
    # 5 - acdeg, acdfg, abdfg
    # 6 - abcefg, abdefg, abcdfg
    # 7 - abcdefg

    # For this problem, we can directly figure out each signal wire.

    # a = {3} - {2}
    # cf = {2}
    # bd = {4} - {2}
    # adg = common of {acdeg, acdfg, abdfg}
    # dg = adg - a
    # abfg = common of {abcefg, abdefg, abcdfg}
    # bfg = abfg - a
    # g = common of {bfg, dg}
    # d = dg - g
    # b = bd - d
    # bf = bfg - g
    # f = bf - b
    # c = cf - f
    # e is the remaining one.


    displayed = entry[:10]

    d3 = [d for d in displayed if len(d) == 3][0]
    d2 = [d for d in displayed if len(d) == 2][0]
    d4 = [d for d in displayed if len(d) == 4][0]
    d5 = [d for d in displayed if len(d) == 5]
    d6 = [d for d in displayed if len(d) == 6]

    a = set(d3) - set(d2)
    cf = set(d2)
    bd = set(d4) - cf

    adg = set(d5[0])
    for i in range(1, 3):
        adg = adg & set(d5[i])

    dg = adg - a
    abfg = set(d6[0])
    for i in range(1, 3):
        abfg = abfg & set(d6[i])

    bfg = abfg - a
    g = bfg & (dg)
    d = dg - g
    b = bd - d
    bf = bfg - g
    f = bf - b
    c = cf - f
    e = set("abcdefg") - (a | b | c | d | f | g)

    originals = ['abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 
            'abdefg', 'acf', 'abcdefg', 'abcdfg']

    originals = [''.join(sorted(o)) for o in originals]

    mapping = {}
    for pr in zip([a, b, c, d, e, f, g], "abcdefg"):
        mapping[min(pr[0])] = pr[1]

    ret = 0
    for e in entry[-4:]:
        decoded = ''.join(sorted(mapping[c] for c in e))
        ret = 10 * ret + originals.index(decoded)

    return ret


def main():
    print(sum(decode(entry) for entry in readInputData()))


if __name__ == '__main__':
    main()

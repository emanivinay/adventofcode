P = (1 << 31) - 1

def generator_sequence(start, factor, sequence_filter_factor=1):
    # start * (factor ^ i) % P
    cur = start
    while True:
        cur = cur * factor % P
        if cur % sequence_filter_factor == 0:
            yield cur


def main():
    seq_A = generator_sequence(512, 16807)
    seq_B = generator_sequence(191, 48271)

    ret1 = 0
    for _ in range(40_000_000):
        a = next(seq_A)
        b = next(seq_B)
        if (a & 0xFFFF) == (b & 0xFFFF):
            ret1 += 1
    
    print(ret1)

    ret2 = 0
    seq_A = generator_sequence(512, 16807, 4)
    seq_B = generator_sequence(191, 48271, 8)
    for _ in range(5_000_000):
        a = next(seq_A)
        b = next(seq_B)
        if (a & 0xFFFF) == (b & 0xFFFF):
            ret2 += 1
    print(ret2)


if __name__ == '__main__':
    main()
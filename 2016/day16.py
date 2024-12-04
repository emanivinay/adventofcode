DATA_LENGTH_NEEDED = 35651584

array = ['1'] * (3 * DATA_LENGTH_NEEDED + 10)


def generate_dragon_data(initial, min_length):
    array_pos = 0
    for c in initial:
        array[array_pos] = c
        array_pos += 1
    
    while array_pos < min_length:
        N = array_pos
        array[array_pos] = '0'
        array_pos += 1
        for i in range(N):
            c = '1' if array[N - 1 - i] == '0' else '0'
            array[array_pos] = c
            array_pos += 1


def compute_checksum(length):
    while length % 2 == 0:
        for i in range(length // 2):
            a, b = array[2 * i : 2 * i + 2]
            array[i] = '1' if a == b else '0'
        length //= 2
    
    return length


def main():
    generate_dragon_data('11011110011011101', DATA_LENGTH_NEEDED)
    checksum_length = compute_checksum(DATA_LENGTH_NEEDED)

    # part 2
    print(''.join(array[:checksum_length]))


if __name__ == '__main__':
    main()
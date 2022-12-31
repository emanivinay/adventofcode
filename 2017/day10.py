import sys

def flip_span(chain, start_pos, length, N):
    for i in range(length // 2):
        a, b = (start_pos + i) % N, (start_pos + N + length - 1 - i) % N
        chain[a], chain[b] = chain[b], chain[a]


def knot_hash(N, lengths, iterations=1):
    cur_pos, chain, skip_size = 0, list(range(N)), 0
    for _ in range(iterations):
        for length in lengths:
            flip_span(chain, cur_pos, length, N)
            cur_pos = (cur_pos + length + skip_size) % N
            skip_size += 1

    return chain


def get_dense_hash(sparse_hash, N):
    ret = [0] * (N // 16)
    for i in range(N // 16):
        for j in range(16):
            ret[i] = ret[i] ^ sparse_hash[i * 16 + j]
    return ret


def main():
    puzzle_data = sys.stdin.read().strip()
    N = 256

    # part 2
    lengths = [ord(c) for c in puzzle_data] + [17, 31, 73, 47, 23]
    sparse_hash = knot_hash(N, lengths, 64)
    dense_hash = get_dense_hash(sparse_hash, N)
    for v in dense_hash:
        a, b = v // 16, v % 16
        print(hex(a)[2:], hex(b)[2:], end='', sep='')
    print()


if __name__ == '__main__':
    main()
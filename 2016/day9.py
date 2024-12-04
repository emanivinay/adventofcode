import sys


def decompress(compressed, recursive_fn=len):
    ret, i = 0, 0
    N = len(compressed)

    while i < N:
        if compressed[i] == '(':
            closing = compressed.index(')', i)
            span, rep = compressed[i + 1 : closing].split('x')
            span, rep = int(span), int(rep)
            # data part is closing + 1 ... closing + span
            ret += recursive_fn(compressed[closing + 1 : closing + span + 1]) * rep
            i = closing + span + 1
        else:
            ret += 1
            i += 1
    
    return ret


def main():
    compressed = sys.stdin.read()
    decompressed = decompress(compressed)

    # part 1
    print(decompressed)

    # part 2
    def recurse(s):
        return decompress(s, recurse)

    decompressed = decompress(compressed, recurse)
    print(decompressed)


if __name__ == '__main__':
    main()

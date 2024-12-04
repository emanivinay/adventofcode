FIRST_ROW = '.^^^^^.^^^..^^^^^...^.^..^^^.^^....^.^...^^^...^^^^..^...^...^^.^.^.......^..^^...^.^.^^..^^^^^...^.'


buffer = ['.'] * len(FIRST_ROW)
prev_row = buffer[:]
W = len(FIRST_ROW)

def build_next_row():
    safe = 0
    row = prev_row
    for i in range(W):
        a = '.' if i == 0 else row[i - 1]
        b = row[i]
        c = '.' if i == W - 1 else row[i + 1]
        cnt = (a == '^') + (b == '^') + (c == '^')
        if cnt == 1 and b != '^':
            buffer[i] = '^'
        elif cnt == 2 and (b == '^'):
            buffer[i] = '^'
        else:
            buffer[i] = '.'
            safe += 1
    return safe


def main():
    H_LARGE = 400000

    global prev_row, buffer
    prev_row = list(FIRST_ROW)
    num_safe_tiles = FIRST_ROW.count('.')
    for i in range(1, H_LARGE):
        num_safe_tiles += build_next_row()
        buffer, prev_row = prev_row, buffer
    
    # part 2
    print(num_safe_tiles)


if __name__ == '__main__':
    main()
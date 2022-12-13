import sys

def tokenize(line):
    i = 0
    while i < len(line):
        if line[i] in '[]':
            yield line[i]
            i += 1
        elif line[i].isspace() or line[i] == ',':
            i += 1
        else:
            num = 0
            while i < len(line) and line[i].isdigit():
                num = 10 * num + int(line[i])
                i += 1
            yield num


def parse_line(line):
    levels = [[]]
    for token in tokenize(line):
        if token == '[':
            levels.append([])
        elif token == ']':
            top_level = levels.pop()
            levels[-1].append(top_level)
        else:
            levels[-1].append(token)

    return levels[0][0]


def compare(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a - b
    elif isinstance(a, int):
        return compare([a], b)
    elif isinstance(b, int):
        return compare(a, [b])
    else:
        na = len(a)
        nb = len(b)
        for i in range(min(na, nb)):
            if a[i] != b[i]:
                return compare(a[i], b[i])
        
        return na - nb


def main():
    lines = [parse_line(line) for line in sys.stdin.read().split('\n') if line.strip()]
    pairs = list(zip(lines, lines[1:]))[::2]
    
    # part 1
    ret = 0
    for i, (a, b) in enumerate(pairs):
        if compare(a, b) <= 0:
            ret += i + 1
    print(ret)

    # part 2, O(N^2) sort by custom comparator
    lines += [[[2]], [[6]]]
    N = len(lines)
    for i in range(N):
        for j in range(i + 1, N):
            if compare(lines[i], lines[j]) > 0:
                lines[i], lines[j] = lines[j], lines[i]
    
    a, b = -1, -1
    for i in range(N):
        if lines[i] == [[2]]:
            a = i + 1
        elif lines[i] == [[6]]:
            b = i + 1
    
    print(a * b)

if __name__ == '__main__':
    main()
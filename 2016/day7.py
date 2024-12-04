import sys


def check_if_abba(s):
    N = len(s)
    for i in range(N - 3):
        a, b, c, d = s[i : i + 4]
        if b == c and a == d and a != b:
            return True
    return False


def parse_inner_outer_parts(s):
    inside = False
    inner, outer, part = [], [], []
    for c in s.strip():
        if c == '[':
            if part:
                outer.append(''.join(part))
            inside = True
            part = []
        elif c == ']':
            if part:
                inner.append(''.join(part))
            inside = False
            part = []
        else:
            part.append(c)

    if part:
        outer.append(''.join(part))
    return (inner, outer)


def main():
    # part 1
    ret = 0
    ret2 = 0
    for line in sys.stdin.readlines():
        inner, outer = parse_inner_outer_parts(line.strip())
        if any(check_if_abba(part) for part in outer) and all(not check_if_abba(part) for part in inner):
            ret += 1
        
        good = False
        for a in range(26):
            for b in range(26):
                if a == b:
                    continue
                aa, bb = chr(ord('a') + a), chr(ord('a') + b)
                aba = f'{aa}{bb}{aa}'
                bab = f'{bb}{aa}{bb}'
                if any(aba in part for part in outer) and any(bab in part for part in inner):
                    good = True
        
        ret2 += good
    
    print(ret, ret2)
            

if __name__ == '__main__':
    main()
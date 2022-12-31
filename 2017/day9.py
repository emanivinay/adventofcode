import sys

def main():
    inside_garbage = False
    depth, last_char = 0, 'a'

    removed, total_score = 0, 0
    for c in sys.stdin.read().strip():
        if last_char == '!':
            last_char = 'a'
            continue

        if inside_garbage:
            if c == '>':
                inside_garbage = False
            else:
                removed += c != '!'
            last_char = c
            continue

        if c == '<':
            inside_garbage = True
        elif c == '{':
            depth += 1
        elif c == '}':
            total_score += depth
            depth -= 1
        
        last_char = c

    # parts 1 and 2
    print(total_score, removed)

main()
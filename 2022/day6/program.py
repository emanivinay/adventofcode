import sys

# Get the first position in stream with last N characters unique
def first_position_with_n_unique(s, N):
    for i in range(N, len(s)):
        if len(set(s[i - N : i])) == N:
            return i

def main():
    input = sys.stdin.read()
    print(first_position_with_n_unique(input, 4))
    print(first_position_with_n_unique(input, 14))

if __name__ == '__main__':
    main()
def main():
    data = [l.strip() for l in open('input.txt').readlines()]

    PAIRS = ["<>", "{}", "()", "[]"]
    VALUES = [4, 3, 1, 2]
    ERRORS = [25137, 1197, 3, 57]

    errorMap = dict((pr[1], err) for pr, err in zip(PAIRS, ERRORS))
    valueMap = dict((pr[1], val) for pr, val in zip(PAIRS, VALUES))
    pairMap = dict(PAIRS)


    values = []
    totalError = 0

    for line in data:
        stack = []
        error = 0
        for c in line:
            if c in errorMap:
                if not stack or pairMap[stack[-1]] != c:
                    error = errorMap[c]
                    break
                stack.pop()
            else:
                stack.append(c)

        totalError += error
        value = -1
        if error == 0 and stack:
            value = 0
            while stack:
                value = 5 * value + valueMap[pairMap[stack.pop()]]
            values.append(value)


    print(totalError, sorted(values)[len(values) // 2])


if __name__ == '__main__':
    main()

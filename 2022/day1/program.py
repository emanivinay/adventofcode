def group_items(lines):
    items, cur = [0], 0
    for line in lines + ['']:
        if not line:
            items.append(0)
            cur = 0
        else:
            items[-1] += int(line)
    
    return items


def main():
    lines = [line.strip() for line in open('input1.txt').readlines()]
    elves = sorted(group_items(lines), reverse=True)

    # input1
    print(elves[0])

    # input2
    print(elves[0] + elves[1] + elves[2])


if __name__ == '__main__':
    main()
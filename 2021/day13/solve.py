def main():
    points = []
    for _ in range(887):
        x, y = input().split(',')
        x = int(x)
        y = int(y)
        points.append((x, y))

    input()
    for it in range(12):
        inst = input().split()[2]
        d, t = inst.split('=')
        t = int(t)
        for i, (x, y) in enumerate(points):
            if d == 'x' and x > t:
                points[i] = (2 * t - x, y)
            elif d == 'y' and y > t:
                points[i] = (x, 2 * t - y)


    rep = '#'
    print(ord(rep))
    grid = [[' '] * 200 for _ in range(200)]
    for x,y in points:
        grid[y][x] = rep
    
    for row in grid:
        if rep in row:
            while row[-1] != rep:
                row.pop()
            print(''.join(row))


main()

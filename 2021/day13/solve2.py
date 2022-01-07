points, folds = open('input.txt').read().split('\n\n')
points = [tuple(map(int, point.split(','))) for point in points.splitlines()]
folds = [(axis[-1], int(val)) for fold in folds.splitlines() for axis, val in [fold.split('=')]]

for axis, val in folds:
    for i, (x, y) in enumerate(points):
        if axis == 'x' and x > val:
            points[i] = (2 * val - x, y)
        elif axis == 'y' and y > val:
            points[i] = (x, 2 * val - y)

    print(len(set(points)))

print('\n'.join(''.join('█' if (x, y) in points else ' ' for x in range(40)) for y in range(6)))

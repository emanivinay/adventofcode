
"""

Advent of Code 2021 - Day 17

"""

from itertools import product

x_min, x_max = 57, 116
y_min, y_max = -198, -148

# Part 1 / Part 2

pairs = product(range(x_max + 1), range(y_min, abs(y_min) + 1))
p1 = 0
total = 0
for x_velocity, y_velocity in pairs:
    x_init, y_init = 0, 0
    y = [y_init]
    xo = x_velocity
    yo = y_velocity
    while x_init <= x_max and y_init >= y_min:
        x_init += x_velocity
        y_init += y_velocity
        y.append(y_init)

        # check
        if x_min <= x_init <= x_max and y_min <= y_init <= y_max:
            total += 1
            if max(y) > p1:
                p1 = max(y)
            break

        if x_velocity > 0:
            x_velocity -= 1

        y_velocity -= 1

print(f'Advent of Code Day 17 Answer Part 1: {p1}')

# Part 2

print(f'Advent of Code Day 17 Answer Part 2: {total}')

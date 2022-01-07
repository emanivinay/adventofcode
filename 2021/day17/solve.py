def launch(vx, vy, xl, xr, y1, y2):
    # y1, y2 denote depth below the surface
    x, y = 0, 0
    zone_reached, highest = 0, 0
    while y >= -y2 and x <= xr:
        highest = max(highest, y)
        if xl <= x <= xr and -y2 <= y <= -y1:
            zone_reached = 1

        x, y = x + vx, y + vy
        vy -= 1
        if vx > 0:
            vx -= 1

    return (zone_reached, highest)


def main():
    xl, xr = 57, 116
    y1, y2 = 148, 198

    besty, total = 0, 0
    for vx in range(xr + 1):
        for vy in range(-200, 200):
            reached, y = launch(vx, vy, xl, xr, y1, y2)
            if reached:
                total += 1
                besty = max(besty, y)

    print(total, besty)


main()

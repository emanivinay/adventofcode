import sys


def simulate(instructions):
    t, cur_x = 1, 1
    instant_values = [0] * 256
    for instr in instructions:
        if instr == 'noop':
            instant_values[t] = cur_x
            t = t + 1
        else:
            incr_by = int(instr.split()[1])
            instant_values[t] = instant_values[t + 1] = cur_x
            t, cur_x = t + 2, cur_x + incr_by

    return instant_values


def main():
    instructions = [line.strip() for line in sys.stdin.read().split('\n')]
    x_values = simulate(instructions)

    # part 1
    print(sum(x_values[t] * t for t in range(20, 221, 40)))

    # part 2
    final_image = [[' '] * 40 for _ in range(6)]
    for t in range(1, 241):
        # sprite left and right ends during t, clipped to [0, 40) space
        left_end, right_end = (max(x_values[t] - 1, 0), min(x_values[t] + 1, 39))
        pixel_x, pixel_y = (t - 1) % 40, (t - 1) // 40
        if left_end <= pixel_x <= right_end:
            final_image[pixel_y][pixel_x] = '#'

    for y in range(6):
        print(''.join(final_image[y]))
    
if __name__ == '__main__':
    main()
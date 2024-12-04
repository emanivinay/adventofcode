import sys

NUM_ROBOTS = 210
NUM_VALUES = 100


def simulate_step(robots, robot_programs, output_bins):
    for i in range(NUM_ROBOTS):
        if len(robots[i]) == 2:
            low, high = sorted(robots[i])
            robots[i].clear()
            lowp, highp = robot_programs[i]
            if lowp[0] == 'output':
                output_bins[lowp[1]] = low
            else:
                robots[lowp[1]].append(low)
            
            if highp[0] == 'output':
                output_bins[highp[1]] = high
            else:
                robots[highp[1]].append(high)
            
            return True
    
    return False


def main():
    # Each robot is an array of chip values it's currently in possession of.
    robots = [[] for _ in range(NUM_ROBOTS)]

    output_bins = [-1] * NUM_VALUES

    # Each program is a pair of low & high value recipients e.g., (bot 34, output 3)
    robot_programs = dict()

    for line in sys.stdin.readlines():
        tokens = line.split()
        if tokens[0] == 'value':
            chip = int(tokens[1])
            receiver = int(tokens[5])
            robots[receiver].append(chip)
        else:
            robot = int(tokens[1])
            low_recvr_type = tokens[5]
            low_recvr_no = int(tokens[6])
            high_recvr_type = tokens[10]
            high_recvr_no = int(tokens[11])
            robot_programs[robot] = ((low_recvr_type, low_recvr_no), (high_recvr_type, high_recvr_no))

    num_steps = 0
    while True:
        num_steps += 1

        for i in range(NUM_ROBOTS):
            if 17 in robots[i] and 61 in robots[i]:
                print('part 1,', i, num_steps)
        
        if not simulate_step(robots, robot_programs, output_bins):
            break

    x, y, z = output_bins[:3]
    print('part 2 -', x * y * z)


if __name__ == '__main__':
    main()
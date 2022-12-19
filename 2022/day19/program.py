import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


def parse_blueprint_line(line):
    tokens = line.split()
    id = int(tokens[1][:-1])
    ore_robot_cost = int(tokens[6])
    clay_robot_cost = int(tokens[12])
    # obs_robot_cost = (ore, clay)
    obs_robot_cost = (int(tokens[18]), int(tokens[21]))
    # geode_robot_cost = (ore, obsidian)
    geode_robot_cost = (int(tokens[-5]), int(tokens[-2]))
    return [id, ore_robot_cost, clay_robot_cost, obs_robot_cost, geode_robot_cost]


MAX_ORES = 200
MAX_CLAY = 200
MAX_OBSIDIAN = 50
MAX_ROBOTS = 33
MAX_TIME = 33

cur_blueprint = None
dp_cache = dict()
[ore_robot_cost, clay_robot_cost, obs_robot_cost, geode_robot_cost] = [0, 0, 0, 0]

def nd_array(*dims):
    if len(dims) == 1:
        return [-1] * dims[0]
    
    return [nd_array(*dims[1:]) for _ in range(dims[0])]

dp_cache = dict()

def f(time, ores, clay, obsidian, ore_robots, clay_robots, obs_robots):
    key = (time, ores, clay, obsidian, ore_robots, clay_robots, obs_robots)

    if key in dp_cache:
        return dp_cache[key]

    if time <= 1:
        return 0

    new_ores = ore_robots
    new_clay = clay_robots
    new_obsidian = obs_robots

    # If new robot manufactured by the factory.
    # ret = f(time - 1, ores + new_ores, clay + new_clay, obsidian + new_obsidian, ore_robots, clay_robots, obs_robots)
    ret = 0
    # if an ore robot is manufactured
    if ores >= ore_robot_cost:
        ret = max(ret, f(time - 1, ores - ore_robot_cost + new_ores, clay + new_clay,
            obsidian + new_obsidian, ore_robots + 1, clay_robots, obs_robots))
    
    # if a clay robot is made
    if ores >= clay_robot_cost:
        ret = max(ret, f(time - 1, ores - clay_robot_cost + new_ores, clay + new_clay,
            obsidian + new_obsidian, ore_robots, clay_robots + 1, obs_robots))
    
    # if a obsidian robot is made
    if ores >= obs_robot_cost[0] and clay >= obs_robot_cost[1]:
        ret = max(ret, f(time - 1, ores - obs_robot_cost[0] + new_ores, clay - obs_robot_cost[1] + new_clay,
            obsidian + new_obsidian, ore_robots, clay_robots, obs_robots + 1))
    
    # if a geode robot is made
    if ores >= geode_robot_cost[0] and obsidian >= geode_robot_cost[1]:
        ret = max(ret, (time - 1) + f(time - 1, ores - geode_robot_cost[0] + new_ores, clay + new_clay,
            obsidian - geode_robot_cost[1] + new_obsidian, ore_robots, clay_robots, obs_robots))
    
    for nt in range(1, time + 1):
        ret = max(ret, f(time - nt, ores + new_ores * nt, clay + new_clay * nt, obsidian + nt * new_obsidian,
        ore_robots, clay_robots, obs_robots))

    dp_cache[key] = ret
    return ret


def max_geodes2(blueprint):
    global cur_blueprint
    cur_blueprint = blueprint
    global ore_robot_cost, clay_robot_cost, obs_robot_cost, geode_robot_cost
    [_, ore_robot_cost, clay_robot_cost, obs_robot_cost, geode_robot_cost] = cur_blueprint

    queue = collections.deque()
    queue.append((24, 0, 0, 0, 1, 0, 0, 0))
    ret = 0
    while queue:
        t, ores, clay, obsidian, ore_bots, clay_bots, obs_bots, geodes = queue.popleft()
        if t == 0:
            ret = max(ret, geodes)
            continue

        queue.append((t - 1, ores + ore_bots, clay + clay_bots, obsidian + obs_bots, ore_bots, clay_bots, obs_bots, geodes))

        if ores >= ore_robot_cost:
            queue.append((t - 1,
                ores - ore_robot_cost + ore_bots, 
                clay + clay_bots,
                obsidian + obs_bots,
                ore_bots + 1,
                clay_bots,
                obs_bots,
                geodes))
        
        if ores >= clay_robot_cost:
            queue.append((t - 1,
                ores - clay_robot_cost + ore_bots,
                clay + clay_bots,
                obsidian + obs_bots,
                ore_bots, clay_bots + 1, obs_bots, geodes))
        
        if ores >= obs_robot_cost[0] and clay >= obs_robot_cost[1]:
            queue.append((t - 1, 
                ores - obs_robot_cost[0] + ore_bots,
                clay - obs_robot_cost[1] + clay_bots,
                obsidian + obs_bots,
                ore_bots, clay_bots, obs_bots + 1, geodes))
        
        if ores >= geode_robot_cost[0] and obsidian >= geode_robot_cost[1]:
            queue.append((t - 1, 
                ores - geode_robot_cost[0] + ore_bots,
                clay + clay_bots,
                obsidian - geode_robot_cost[1] + obs_bots,
                ore_bots, clay_bots, obs_bots, geodes + t - 1))

    return ret

def max_geodes(blueprint):
    global dp_cache
    dp_cache.clear()

    global cur_blueprint
    cur_blueprint = blueprint

    global ore_robot_cost, clay_robot_cost, obs_robot_cost, geode_robot_cost
    [_, ore_robot_cost, clay_robot_cost, obs_robot_cost, geode_robot_cost] = cur_blueprint

    return f(24, 0, 0, 0, 1, 0, 0)


def main():
    input_lines = sys.stdin.read().split('\n')
    blueprints = [parse_blueprint_line(line.strip()) for line in input_lines]
    ret = 0
    for blueprint in blueprints:
        ret += blueprint[0] * max_geodes(blueprint)
    
    print(ret)


if __name__ == '__main__':
    main()
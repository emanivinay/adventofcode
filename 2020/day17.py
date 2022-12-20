PUZZLE = '''..#..#.#
##.#..#.
#....#..
.#..####
.....#..
...##...
.#.##..#
.#.#.#.#'''


def gen_neighbors(x, y, z, w):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                for dw in range(-1, 2):
                    if dx != 0 or dy != 0 or dz != 0 or dw != 0:
                        yield (x + dx, y + dy, z + dz, w + dw)


def simulate_cycle(active_cube_set):
    next_active_set = set()
    inactive_candidate_set = set()

    for cube in active_cube_set:
        active_neighbor_count = 0
        for neighbor in gen_neighbors(*cube):
            if neighbor in active_cube_set:
                active_neighbor_count += 1
            else:
                inactive_candidate_set.add(neighbor)
        
        if 2 <= active_neighbor_count <= 3:
            next_active_set.add(cube)

    # consider inactive neighbors that're candidates to turn active in this cycle.
    for cube in inactive_candidate_set:
        active_neighbor_count = sum(neighbor in active_cube_set for neighbor in gen_neighbors(*cube))
        if active_neighbor_count == 3:
            next_active_set.add(cube)
    
    return next_active_set


def main():
    active_cubes = set()

    N = 8
    puzzle = PUZZLE.split()

    for i in range(N):
        for j in range(N):
            if puzzle[i][j] == '#':
                active_cubes.add((j, N - 1 - i, 0, 0))
    
    # part 1
    for _ in range(6):
        active_cubes = simulate_cycle(active_cubes)
    
    print(len(active_cubes))


main()
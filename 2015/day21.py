# Any item = (cost, damage, defense)
# character = (hit points, damage, defense)
from itertools import combinations

WEAPONS = [(x, i + 4, 0) for i, x in enumerate([8, 10, 25, 40, 74])]
ARMOR = [(x, 0, i + 1) for i, x in enumerate([13, 31, 53, 75, 102])] + [(0, 0, 0)] # (not choosing any armor item)
RINGS = [(25 << i, i + 1, 0) for i in range(3)] + [(20 << i, 0, i + 1) for i in range(3)]


def simulate_duel(boss, you):
    hit_boss, damage_boss, defense_boss = boss
    hit_you, damage_you, defense_you = you

    while hit_boss > 0 and hit_you > 0:
        hit_boss -= max(1, damage_you - defense_boss)
        if hit_boss <= 0:
            return True
        
        hit_you -= max(1, damage_boss - defense_you)
        if hit_you <= 0:
            return False


def main():
    boss = (103, 9, 2)
    ret = 1 << 50
    ret2 = 0

    for weapon in WEAPONS:
        for armor_item in ARMOR:
            for r in range(3):
                for rings in combinations(RINGS, r):
                    cost, damage, defense = [weapon[i] + armor_item[i] + sum(ring[i] for ring in rings) for i in range(3)]
                    if simulate_duel(boss, (100, damage, defense)):
                        ret = min(ret, cost)
                    else:
                        ret2 = max(ret2, cost)

    print(ret, ret2)


main()
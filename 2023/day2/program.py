import sys
import collections
import itertools
import functools

def split_line_to_type(line, type_converter):
    return [type_converter(word) for word in line.split()]


split_ints = lambda line: split_line_to_type(line, int)


COLORS = ['red', 'green', 'blue']


def parse_game_line(line: str):
    game_id_str, rounds_str = line.split(': ')
    game_id = int(game_id_str.split()[1])
    rounds = rounds_str.split('; ')
    round_counts = []
    for round in rounds:
        colors = round.split(', ')
        count = [0, 0, 0]
        for color in colors:
            cnt, color2 = color.split()
            cnt = int(cnt)
            color_id = COLORS.index(color2)
            count[color_id] = cnt
        round_counts.append(count)

    return (game_id, round_counts)


def main():
    input_lines = sys.stdin.read().split('\n')

    # parts 1 and 2
    ret, ret2 = 0, 0
    for line in input_lines:
        game_id, rounds = parse_game_line(line)
        if all((r <= 12 and g <= 13 and b <= 14) for [r, g, b] in rounds):
            ret += game_id
        
        min_r, min_g, min_b = [max(round[i] for round in rounds) for i in range(3)]
        ret2 += min_r * min_g * min_b

    print(ret, ret2)


if __name__ == '__main__':
    main()

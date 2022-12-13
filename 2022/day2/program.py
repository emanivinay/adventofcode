import sys

# Opponent always plays first - A, B and C mean R, P and S respectively
# Player plays second - X, Y and Z mean different things for parts 1 and 2
#   Part 1 - X, Y and Z mean R, P and S
#   Part 2 - X, Y and Z mean lose, draw and win

# Constants for winning, draw, losing
[WINNING, DRAWING, LOSING] = [0, 1, 2]

# winning, drawing, losing choices for each opponent play (in that order)
PLAY_CHOICES = {
    'A' : 'YXZ',
    'B' : 'ZYX',
    'C' : 'XZY',
}

# one of the WINNING, DRAWING, LOSING outcomes
# a is in (A, B, C) and b is in (X, Y, Z)
def outcome(a, b):
    return PLAY_CHOICES[a].index(b)


# part 1 score
def compute_score(a, b):
    choice_score = ord(b) - ord('X') + 1
    outcome_score = (2 - outcome(a, b)) * 3
    return outcome_score + choice_score


# part 2 score
def compute_score2(a, b):
    o = ord('Z') - ord(b)
    to_play = PLAY_CHOICES[a][o]
    return compute_score(a, to_play)


def main():
    total_score1, total_score2 = 0, 0

    for line in sys.stdin.readlines():
        opp, you = line.split()
        total_score1 += compute_score(opp, you)
        total_score2 += compute_score2(opp, you)
    
    print(total_score1, total_score2)


if __name__ == '__main__':
    main()
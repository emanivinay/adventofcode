def say_sequence(start_seq, n_terms, interesting_index):
    last_two_times_map = dict()
    ret = []
    last_term = -1
    for i in range(n_terms):
        if i < len(start_seq):
            new_term = start_seq[i]
        else:
            old, new = last_two_times_map[last_term]
            new_term = 0 if old < 0 else new - old

        a, b = last_two_times_map.get(new_term, (-1, -1))
        last_two_times_map[new_term] = (b, i)
        last_term = new_term

        if i == interesting_index:
            ret.append(new_term)

    ret += [last_term]
    return ret


def main():
    # parts 1 and 2
    sequence = say_sequence([7, 12, 1, 0, 16, 2], 30000000, 2019)
    print(sequence[0], sequence[1])


main()

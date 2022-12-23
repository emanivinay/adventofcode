import sys
import collections
import functools


def parse_rule_line(line):
    tokens = line.split()
    head = int(tokens[0][:-1])
    if 'a' in line or 'b' in line:
        terminal = tokens[1][1:-1]
        return (head, 'terminal', terminal)

    rest = ' '.join(tokens[1:])
    derivations = []
    parts = rest.split(' | ')
    for part in parts:
        derivations.append(list(int(w) for w in part.split()))
    
    return (head, 'derived', derivations)


def simulate(generated_matches, rules, max_candidate_size, excluded_nodes):
    iter = 0
    while True:
        iter += 1
        print(iter)

        updated = False
        for head, rule in rules.items():
            if head not in excluded_nodes and rule[0] == 'derived':
                prev_generation_count = len(generated_matches[head])
                derivations = rule[1]
                new_generation_matches = set()
                for deriv in derivations:
                    if all(member in generated_matches for member in deriv):
                        new_gen = set([""])
                        for member in deriv:
                            matched_parts = generated_matches[member]
                            new_gen = list(prefix + part for prefix in new_gen for part in matched_parts
                                if len(prefix + part) <= max_candidate_size)
                        
                        new_generation_matches.update(new_gen)
                
                generated_matches[head].update(new_generation_matches)
                if prev_generation_count < len(generated_matches[head]):
                    updated = True
        
        if not updated:
            break


def main():
    lines = sys.stdin.readlines()

    rules = dict()
    candidates = []
    for line in lines:
        if '"' in line:
            head, rule_type, derivation = parse_rule_line(line.strip())
            rules[head] = (rule_type, derivation)
        elif 'a' in line or 'b' in line:
            candidates.append(line.strip())
        elif line.strip():
            head, rule_type, derivation = parse_rule_line(line.strip())
            rules[head] = (rule_type, derivation)
    
    max_candidate_size = max(len(candidate) for candidate in candidates)
    generated_matches = collections.defaultdict(set)

    # Seed generated with terminals
    for head, rule in rules.items():
        if rule[0] == 'terminal':
            generated_matches[head].add(rule[1])

    # simulate(generated_matches, rules, max_candidate_size)
    # print(sum(candidate in generated_matches[0] for candidate in candidates))

    N = max(rules.keys()) + 1
    depends = [[False] * N for _ in range(N)]
    for i in range(N):
        depends[i][i] = True
    
    for node in range(N):
        if rules[node][0] == 'derived':
            for derivation in rules[node][1]:
                for dependency in derivation:
                    depends[node][dependency] = True

    for i in range(N):
        for j in range(N):
            for k in range(N):
                if depends[j][i] and depends[i][k]:
                    depends[j][k] = True
    
    simulate(generated_matches, rules, max_candidate_size, [0, 8, 11])

    # 0 -> 8 11
    # 8 -> 42+
    # 11 -> 42[n] 31[n]

    # 0 -> 42^m 42^n 31^n, m >= 1, n >= 1
    set42 = generated_matches[42]
    set31 = generated_matches[31]

    @functools.lru_cache(maxsize=None)
    def f(text, cand, n):
        if not text or n == 0:
            return n == 0 and not text
        
        st = set42 if cand == 42 else set31
        for prefix in st:
            if text.startswith(prefix) and f(text[len(prefix):], cand, n - 1):
                return True
        
        return False


    @functools.lru_cache(maxsize=None)
    def g(text, cand):
        if not text:
            return set([0])
        
        st = set42 if cand == 42 else set31
        reps = set()
        for n in range(1, len(text) + 1):
            if f(text, cand, n):
                reps.add(n)
        return reps

    ret = 0
    for candidate in candidates:
        matches = False
        n = len(candidate)
        
        for p in range(1, n + 1):
            if matches:
                break
            if not g(candidate[:p], 42):
                continue
            for q in range(1, n - p + 1):
                if matches:
                    break
                for r in range(1, n - p - q + 1):
                    if g(candidate[p:p + q], 42) & g(candidate[p + q:], 31):
                        matches = True
                        break

        ret += matches
    
    print(ret)

main()
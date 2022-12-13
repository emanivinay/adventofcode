import sys
from collections import deque, Counter
from hashlib import md5


def main():
    SALT = 'ngcjuoqr'
    HEXA = 16
    TRIPLES = [hex(d)[2:] * 3 for d in range(HEXA)]
    QUINTIPLES = [hex(d)[2:] * 5 for d in range(HEXA)]

    tail_hashes = deque()
    quintiple_counter = Counter()
    keys, index = [], 0
    while len(keys) < 64:
        cur_hash = md5(f'{SALT}{index}'.encode()).hexdigest()
        for _ in range(2016):
            cur_hash = md5(cur_hash.encode()).hexdigest()
        
        counter_array = []
        tail_hashes.append((cur_hash, index, counter_array))
        for d in range(HEXA):
            if QUINTIPLES[d] in cur_hash:
                quintiple_counter[d] += 1
                counter_array.append(d)
        if len(tail_hashes) > 1000:
            head_hash, head_index, counter_array = tail_hashes.popleft()
            for d in counter_array:
                quintiple_counter[d] -= 1
            
            L = len(head_hash)
            for i in range(L - 2):
                if head_hash[i] == head_hash[i + 1] == head_hash[i + 2]:
                    d = int(head_hash[i], 16)
                    if quintiple_counter[d] > 0:
                        keys.append((head_hash, head_index))
                    break
        index += 1
        print(index)

    print(keys[-1])

main()
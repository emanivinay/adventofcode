MAX = 3000000


def pre_compute():
    factors = [x for x in range(MAX + 1)]
    for i in range(2, MAX + 1):
        if factors[i] == i:
            for j in range(2 * i, MAX + 1, i):
                factors[j] = i
    
    return factors


def get_divisor_sum(n, factors):
    ret = 1
    while n > 1:
        f, e = factors[n], 0
        while n % f == 0:
            n, e = n // f, e + 1
        ret *= (f ** (e + 1) - 1) // (f - 1)
    return ret


def main():
    factors = pre_compute()
    for n in range(1, MAX + 1):
        if get_divisor_sum(n, factors) >= 3600 * 1000:
            print(n)
            break
    
    # elf i visits houses (i, 2 * i ... 50 * i)
    # house x = a * b (1 <= a <= 50) => elf b visits it and gives gifts worth 11 * b
    gifts = [0] * (MAX + 1)
    for a in range(1, 51):
        for house in range(a, MAX + 1, a):
            gifts[house] += (house // a)
    
    for h in range(1, MAX + 1):
        if 11 * gifts[h] >= 3600 * 10000:
            print(h)
            break

main()
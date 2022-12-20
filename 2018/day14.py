def simulate(num_recipes):
    recipes = [3, 7]
    N, fst, snd = 2, 0, 1
    while N < num_recipes:
        a = recipes[fst]
        b = recipes[snd]
        sum = a + b
        if sum < 10:
            recipes.append(sum)
            N += 1
        else:
            N += 2
            recipes.append(sum // 10)
            recipes.append(sum % 10)

        fst = (fst + 1 + a) % N
        snd = (snd + 1 + b) % N
    
    return recipes


RECIPES = 440231

def main():
    recipes = simulate(RECIPES + 10)
    # part 1
    print(''.join(str(recipes[i]) for i in range(RECIPES, RECIPES + 10)))

    DIGITS = [int(d) for d in str(RECIPES)]

    

main()
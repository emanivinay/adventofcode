def simulate(num_recipes, recipes, fst=0, snd=1):
    N, fst, snd = len(recipes), 0, 1
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
    recipes = simulate(21000000, [3, 7])
    # part 1
    print(''.join(str(recipes[i]) for i in range(RECIPES, RECIPES + 10)))

    # part 2
    recipe_digits = [4, 4, 0, 2, 3, 1]

    for i in range(len(recipes) - 5):
        if recipes[i] == 4 and recipes[i + 1] == 4 and recipes[i + 2] == 0\
            and recipes[i + 3] == 2 and recipes[i + 4] == 3 and recipes[i + 5] == 1:
            print(i)
            break


main()
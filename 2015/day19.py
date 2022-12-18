import sys
from collections import defaultdict
import functools

LARGE = 1 << 50


@functools.lru_cache(maxsize=None)
def split_atoms(atoms_str):
    atoms = []
    i = 0
    while i < len(atoms_str):
        if atoms_str[i] == 'e':
            atoms.append('e')
            i += 1
            continue

        new_atom = atoms_str[i]
        i += 1
        while i < len(atoms_str) and (atoms_str[i].islower()) and atoms_str[i] != 'e':
            new_atom += atoms_str[i]
            i += 1
        atoms.append(new_atom)
    
    return atoms


def main():
    replacements_map = defaultdict(list)
    starting_atoms_str = ''
    for line in sys.stdin.readlines():
        if '=>' in line:
            starter, atoms_str = line.strip().split(' => ')
            replacements_map[starter].append(atoms_str)
        elif line.strip():
            starting_atoms_str = line.strip()
    
    start_atoms = split_atoms(starting_atoms_str)
    single_step_xformations = set()
    for i in range(len(start_atoms)):
        prefix = ''.join(start_atoms[j] for j in range(i))
        suffix = ''.join(start_atoms[j] for j in range(i + 1, len(start_atoms)))
        for replaced_by in replacements_map[start_atoms[i]]:
            single_step_xformations.add(prefix + replaced_by + suffix)
    
    print(len(single_step_xformations))
    target_atoms_str = starting_atoms_str

    seen = set()

    sys.setrecursionlimit(1 << 20)
    dp_cache = dict()
    size = 0
    def f(current_atom_str, l, r):
        target_str = ''.join(start_atoms[l : r])
        if current_atom_str == target_str:
            return 0
        if len(current_atom_str) > len(target_str):
            return LARGE
        if target_str and not current_atom_str:
            return LARGE

        key = current_atom_str, l, r
        if key in dp_cache:
            return dp_cache[key]

        nonlocal size
        size += 1
        if size % 10000 == 0:
            print(size)
        atoms = split_atoms(current_atom_str)
        ret = LARGE
        if len(atoms) == 1:
            for replaced_by in replacements_map[atoms[0]]:
                if replaced_by != current_atom_str:
                    ret = min(ret, 1 + f(replaced_by, l, r))
        else:
            rest_atoms_str = ''.join(atoms[1:])
            for i in range(l, r - 1):
                # first atom => [l, i + 1), rest => [i + 1, r)
                ret = min(ret, f(atoms[0], l, i + 1) + f(rest_atoms_str, i + 1, r))

        dp_cache[key] = ret
        return ret
    
    print(f('e', 0, len(start_atoms)))

main()
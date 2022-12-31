from collections import defaultdict


def parse_tree(lines):
    tree = defaultdict(lambda: {
        'weight': 0,
        'children': [],
        'name': '',
    })
    non_root_set = set()
    for line in lines:
        tokens = line.split()
        name = tokens[0]
        weight = int(tokens[1][1:-1])
        node = tree[name]
        node['weight'] = weight
        node['name'] = name
        if len(tokens) >= 4:
            for child in tokens[3:]:
                child2 = child if not child.endswith(',') else child[:-1]
                non_root_set.add(child2)
                node['children'].append(child2)
    
    root = min(key for key in tree.keys() if key not in non_root_set)
    return (tree, root)


def find_bad_weight(tree, root):
    node = tree[root]

    if not node['children']:
        return (node['weight'], False)

    sub_tree_wts = []
    for child in node['children']:
        wt, found = find_bad_weight(tree, child)
        if found:
            return (wt, True)
        sub_tree_wts.append((wt, child))
    
    sub_tree_wts.sort()
    if sub_tree_wts[0][0] == sub_tree_wts[-1][0]:
        return (sub_tree_wts[0][0] * len(sub_tree_wts) + node['weight'], False)
    else:
        if sub_tree_wts[0][0] == sub_tree_wts[1][0]:
            bad_child = sub_tree_wts[-1][1]
            diff = sub_tree_wts[0][0] - sub_tree_wts[-1][0]
            return (tree[bad_child]['weight'] + diff, True)
        else:
            bad_child = sub_tree_wts[0][1]
            diff = sub_tree_wts[-1][0] - sub_tree_wts[0][0]
            return (tree[bad_child]['weight'] + diff, True)


def main():
    tree, root = parse_tree(line.strip() for line in open('input7.txt').readlines())
    # part 1
    print(root)

    # part 2
    print(find_bad_weight(tree, root)[0])

main()
import sys

SMALL_DIR_SIZE_LIMIT = 100000


def build_fsys(commands):
    root = dict()
    i, cwd = 0, root
    while i < len(commands):
        parts = commands[i].split()[1:]
        i += 1
        if parts[0] == 'ls':
            # read cwd contents list
            while i < len(commands):
                if commands[i][0] == '$':
                    break
                metadata, name = commands[i].split()
                i += 1
                if metadata == 'dir':
                    # sub-dir, create a new dict object and add a parent pointer in it.
                    sub_dir = cwd[name] = dict()
                    sub_dir['..'] = cwd
                else:
                    cwd[name] = int(metadata)
        else:
            # cd into another directory
            new_dir = parts[1]
            if new_dir == '/':
                cwd = root
            else:
                cwd = cwd[new_dir]

    return root


def get_directory_size(node, subtree_processor):
    if isinstance(node, dict):
        ret = 0
        for name, child in node.items():
            if name != '..':
                ret += get_directory_size(child, subtree_processor)
        subtree_processor(ret)
        return ret
    
    return node


def main():
    commands = [line.strip() for line in sys.stdin.readlines()]
    file_system = build_fsys(commands)
    
    small_dirs = []
    all_dirs = []
    def add_dirs(size):
        if size <= SMALL_DIR_SIZE_LIMIT:
            small_dirs.append(size)
        all_dirs.append(size)
    
    # part 1
    used_space = get_directory_size(file_system, add_dirs)
    print(sum(small_dirs))

    # part 2
    TOTAL_SPACE = 70 * 1000 * 1000
    FREE_SPACE_NEEDED = 30 * 1000 * 1000
    free_space = TOTAL_SPACE - used_space
    extra_free_space_needed = max(FREE_SPACE_NEEDED - free_space, 0)
    print(min(size for size in all_dirs if size >= extra_free_space_needed))


if __name__ == '__main__':
    main()
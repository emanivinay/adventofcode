import hashlib

# up, down, left and right
PASSCODE = 'qzthpkfp'

STEPS_BY_DIR = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
}

def get_door_state_in_current_room(path):
    path_str = ''.join(path)
    digest = hashlib.md5((PASSCODE + path_str).encode()).hexdigest()[:4]
    return [digest[i] in 'bcdef' for i in range(4)]


# try going in this order - D, L, R, U
def recurse(y, x, path, result):
    if y < 0 or x < 0 or y >= 4 or x >= 4:
        return

    if y == 3 and x == 3:
        if not result[0] or len(result[0]) > len(path):
            result[0] = path[:]
        result[1] = max(result[1], len(path))
        return

    for dir, is_open in zip("UDLR", get_door_state_in_current_room(path)):
        if is_open:
            path.append(dir)
            dy, dx = STEPS_BY_DIR[dir]
            recurse(y + dy, x + dx, path, result)
            path.pop()


def main():
    result = ["", 0]
    recurse(0, 0, [], result)
    print(''.join(result[0]), result[1])


if __name__ == '__main__':
    main()
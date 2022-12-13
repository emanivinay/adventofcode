from hashlib import md5


def gen_hashes_starting_with_00000(door_id):
    index = 0
    while True:
        door_hash = md5(f'{door_id}{index}'.encode()).hexdigest()
        if door_hash.startswith('00000'):
            yield door_hash
        index += 1


def main():
    DOOR_ID = 'reyedfim'

    # Parts 1 and 2
    password1 = ''
    password2 = ['_'] * 8
    for door_hash in gen_hashes_starting_with_00000(DOOR_ID):
        if len(password1) < 8:
            password1 += door_hash[5]
        index = int(door_hash[5], 16)
        letter = door_hash[6]
        if index < 8 and password2[index] == '_':
            password2[index] = letter
        if len(password1) == 8 and '_' not in password2:
            break
    
    print(password1, ''.join(password2))


if __name__ == '__main__':
    main()
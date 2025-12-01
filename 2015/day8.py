def code_literal_length(s):
    return len(s)


def in_memory_size(s):
    i = 0
    ret = 0
    while i < len(s):
        if s[i] == '"':
            ret += 1
            i += 1
            continue
        if s[i] == '\\':
            if s[i + 1] in ('\\', '\"'):
                ret += 1
                i += 2
                continue
            else:
                assert s[i + 1] == 'x', str(s)
                ret += 1
                i += 4
                continue
        else:
            ret += 1
            i += 1
    return ret - 2

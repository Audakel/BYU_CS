def w2s(word):
    if word is None:
        return '        '

    return array_to_hex_string(word)


def array_to_hex_string(a):
    return ''.join(['{:02x}'.format(x) for x in a.flatten()])


def print_word(word):
    print w2s(word)


def print_state(state):
    transform = state.T

    for i in range(len(transform)):
        print_word(transform[i])

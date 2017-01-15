def mix_columns(state):
    # for each column, compute the new values for each cell by multiplying (ff_multiply) by the matrix:
    # [[ 0x02  0x03  0x01  0x01 ]
    #  [ 0x01  0x02  0x03  0x01 ]
    #  [ 0x01  0x01  0x02  0x03 ]
    #  [ 0x03  0x01  0x01  0x02 ]]

    # for each column in the state (there should only be 4)...
    for c in range(4):
        # get the column from the state
        col = state[c]

        # create a new column (initialized to all 0s)
        mixed_column = np.zeros(4, np.int64)

        # compute the new values doing the matrix multiply
        mixed_column[0] = ff_add(ff_multiply(col[0], 0x02), ff_multiply(col[1], 0x03), col[2], col[3])
        mixed_column[1] = ff_add(col[0], ff_multiply(col[1], 0x02), ff_multiply(col[2], 0x03), col[3])
        mixed_column[2] = ff_add(col[0], col[1], ff_multiply(col[2], 0x02), ff_multiply(col[3], 0x03))
        mixed_column[3] = ff_add(ff_multiply(col[0], 0x03), col[1], col[2], ff_multiply(col[3], 0x02))

        # set the new column in the state
        state[c] = mixed_column

    # return the modified state
    return state


def inv_mix_columns(state):
    # for each column, compute the new values for each cell by multiplying (ff_multiply) by the matrix:
    # [[ 0x0e  0x0b  0x0d  0x09 ]
    #  [ 0x09  0x0e  0x0b  0x0d ]
    #  [ 0x0d  0x09  0x0e  0x0b ]
    #  [ 0x0b  0x0d  0x09  0x0e ]]

    # for each column in the state (there should only be 4)...
    for c in range(4):
        # get the column from the state
        col = state[c]

        # create a new column (initialized to all 0s)
        mixed_column = np.zeros(4, np.int64)

        # compute the new values doing the matrix multiply
        mixed_column[0] = ff_add(ff_multiply(col[0], 0x0e), ff_multiply(col[1], 0x0b), ff_multiply(col[2], 0x0d),
                                 ff_multiply(col[3], 0x09))
        mixed_column[1] = ff_add(ff_multiply(col[0], 0x09), ff_multiply(col[1], 0x0e), ff_multiply(col[2], 0x0b),
                                 ff_multiply(col[3], 0x0d))
        mixed_column[2] = ff_add(ff_multiply(col[0], 0x0d), ff_multiply(col[1], 0x09), ff_multiply(col[2], 0x0e),
                                 ff_multiply(col[3], 0x0b))
        mixed_column[3] = ff_add(ff_multiply(col[0], 0x0b), ff_multiply(col[1], 0x0d), ff_multiply(col[2], 0x09),
                                 ff_multiply(col[3], 0x0e))

        # set the new column in the state
        state[c] = mixed_column

    # return the modified state
    return state


def sub_bytes(state):
    copy = state.copy()

    # replace each byte in the array with it's corresponding value in the S_BOX
    for byte in np.nditer(copy, op_flags=['readwrite']):
        byte[...] = sub_byte(byte, S_BOX)

    return copy


def inv_sub_bytes(state):
    copy = state.copy()

    # replace each byte in the array with it's corresponding value in the INV_S_BOX
    for byte in np.nditer(copy, op_flags=['readwrite']):
        byte[...] = sub_byte(byte, INV_S_BOX)

    return copy


def sub_byte(byte, sub_table):
    # get the low-order value
    low = byte & 0x0f

    # get the high-order value
    high = (byte >> 4) & 0x0f

    # get the replacement value from the S_BOX
    return sub_table[high, low]


def sub_word(word):
    return sub_bytes(word)


def rot_word(word):
    return np.roll(word, 3)


def shift_rows(state):
    # transpose (rotate) the state
    shifted = state.T

    # for each row (was a column) roll it by 4 - row index
    for i in range(4):
        shifted[i] = np.roll(shifted[i], 4 - i)

    return state


def inv_shift_rows(state):
    # transpose (rotate) the state
    shifted = state.T

    # for each row (was a column) roll it by row index
    for i in range(4):
        shifted[i] = np.roll(shifted[i], i)

    return state


def add_round_key(state, round_key):
    # just XOR the corresponding elements of the state and the round key
    return np.bitwise_xor(state, round_key)


def ff_multiply(operand, times):
    # if input or times <= 0, then return 0
    if operand <= 0 or times <= 0:
        return 0

    # if input or times is 1, then return the other
    if operand == 1:
        return times
    if times == 1:
        return operand

    # start with a 0 product that we'll accumulate
    product = 0

    # start at the lowest order bit
    current_bit = MIN_X_TIME_BIT

    # loop until we've hit all the bits of 'times'
    while current_bit <= times:
        # if the current bit of 'times' is set, then do x_time for the current bit, adding the result to the product
        if times & current_bit == current_bit:
            product = ff_add(product, x_time(operand, current_bit))

        # increment the bit (left shift one place)
        current_bit <<= 1

    return product


def x_time(operand, bit=DEFAULT_X_TIME_BIT):
    # if we've hit the minimum bit, then just return the operand
    if bit <= MIN_X_TIME_BIT:
        return operand

    # multiply the operand by 2 (left shift one place), while decrementing the bit (right shift one place)
    return x_time(normalize(operand << 1), bit >> 1)


def normalize(val):
    # if the product is too big, then modulo (just XOR) it by 0x11b
    if val & HIGH_ORDER_BIT == HIGH_ORDER_BIT:
        return val ^ MODULO

    return val


def ff_add(*args):
    # start with 0
    result = 0

    # for each argument...
    for a in args:
        # XOR the argument with the sum
        result ^= a

    # return the sum
    return result


def rcon(i):
    # check if this 'i' is in the cache already, if so then just use that
    if i in R_CON_CACHE:
        return R_CON_CACHE[i]

    # create a new word of all 0s
    result = np.zeros(4, np.uint16)

    # if i is too low, then just return the all 0s
    if i <= 0:
        return result

    # compute the 0th nibble of the word
    result[0] = x_time(1, 1 << (i - 1))

    # save the word in the cache
    R_CON_CACHE[i] = result

    return result

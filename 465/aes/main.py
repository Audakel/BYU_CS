__author__ = 'keith'

import numpy as np
import argparse

N_B = 4
N_R = {4: 10, 6: 12, 8: 14}

MODULO = 0x11b
HIGH_ORDER_BIT = 0x100
MIN_X_TIME_BIT = 0x01
DEFAULT_X_TIME_BIT = 0x02

# these values are obtained directly from the FIPS 197 spec
S_BOX = np.array([[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
                  [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
                  [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
                  [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
                  [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
                  [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
                  [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
                  [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
                  [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
                  [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
                  [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
                  [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
                  [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
                  [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
                  [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
                  [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]],
                 np.uint8)

INV_S_BOX = np.array([[0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
                      [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
                      [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
                      [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
                      [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
                      [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
                      [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
                      [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
                      [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
                      [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
                      [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
                      [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
                      [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
                      [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
                      [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
                      [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]],
                     np.uint8)

R_CON_CACHE = {}


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


class PyCipher:
    def __init__(self):
        self.input_bytes = None
        self.cipher_key = None
        self.is_verbose = False
        self.is_encrypting = True
        self.is_bytes = True
        self.input_string = ''
        self.key_string = ''
        self.key_schedule = None
        self.n_k = 4
        self.n_r = 10

        # parse the arguments
        self.parse_args()

        # prepare the key schedule
        self.prepare_key_schedule()

        # prepare the input
        self.prepare_input()

        # encrypt (or decrypt) the input
        if self.is_encrypting:
            self.encrypt()
        else:
            self.decrypt()

    def parse_args(self):
        # set up the argument parser
        parser = argparse.ArgumentParser(description='This program encrypts (and decrypts) bytes or text using the '
                                                     'Advanced Encryption Standard supporting 128-, 192- and 256-bit'
                                                     'keys',
                                         add_help=True)

        # add an argument to enable verbose output
        parser.add_argument('-v', '--verbose', help='display verbose output', action='store_true')

        # add arguments to set whether encrypting or decrypting
        parser.add_argument('-e', '--encrypt', help='use pychipher for encryption (default)', action='store_true')
        parser.add_argument('-d', '--decrypt', help='use pychipher for decryption', action='store_true')

        # add arguments to set whether input is text or bytes
        parser.add_argument('-b', '--bytes', help='treat input as bytes (default); use 2-digit hexadecimal (0-9, a-f) '
                                                  'sequences to represent bytes value with range from 0 (00) to 255 '
                                                  '(ff)',
                            action='store_true')
        parser.add_argument('-t', '--text', help='treat input as text string with default encoding; enclose input in '
                                                 'quotes',
                            action='store_true')

        # add argument for the input value
        parser.add_argument('-i', '--input', help='the input value to be encrypted or decrypted', required=True)

        # add argument for the cipher key
        parser.add_argument('-k', '--key', help='the key to be used for encryption or decryption; must be expressed as '
                                                'a sequence of hexadecimal characters representing the bytes of the '
                                                '128-, 192-, or 256-bit key',
                            required=True)

        # parse the arguments
        args = parser.parse_args()

        # flip switches according to the arguments
        self.is_verbose = args.verbose
        if self.is_verbose:
            print 'Verbose output is on!'

        # set whether we are encrypting or decrypting
        if args.encrypt and args.decrypt:
            raise Exception('PyCipher can be used to either encrypt or decrypt, but not both.')
        self.is_encrypting = args.encrypt
        self.is_encrypting = not args.decrypt
        if self.is_verbose:
            print 'PyCipher is %s' % ('encrypting' if self.is_encrypting else 'decrypting')

        # set whether the input is bytes or text
        if args.bytes and args.text:
            raise Exception('PyCipher can accept input as bytes or as text, but not both.')
        self.is_bytes = args.bytes
        self.is_bytes = not args.text
        if self.is_verbose:
            print 'PyCipher input is %s' % ('bytes' if self.is_bytes else 'text')

        # save the input
        self.input_string = args.input

        # save the cipher key
        self.key_string = args.key

    def prepare_key_schedule(self):
        if self.is_verbose:
            print 'Checking key...'

        # if the key length is 0, then we can't continue
        key_length = len(self.key_string)
        if key_length == 0:
            raise Exception('Cipher key has no length.  Please supply a valid cipher key.')

        # if the key length is *not* an even number, then we can't use it
        if key_length % 2 is not 0:
            raise Exception('Cipher key has an odd length.  Please supply a valid cipher key.')

        # if the key length is *not* 32 or 48 or 64, then we can't use it
        if key_length not in [32, 48, 64]:
            raise Exception('Cipher key length is invalid.  Cipher key must be one of length: 32 chars (128-bit), 48 '
                            'chars (192-bit), or 64 chars (256-bit)')

        # parse the key string into an array of numbers (bytes, really)
        key_array = np.array([int(self.key_string[i:i + 2], 16) for i in range(0, key_length, 2)])
        self.cipher_key = key_array.reshape(len(key_array) / 4, 4)

        # perform key expansion here?
        self.key_schedule, self.n_k, self.n_r = self.key_expansion(self.cipher_key)

    def key_expansion(self, cipher_key):
        if self.is_verbose:
            print 'Computing key schedule...'

        key_schedule = np.copy(cipher_key)
        n_k = len(cipher_key)
        n_r = n_k + 6

        if self.is_verbose:
            print
            print '               After     After      Rcon      XOR'
            print ' i  Previous  RotWord   SubWord    Value    w/ Rcon   w[i-Nk]    Final'
            print '=== ========  ========  ========  ========  ========  ========  ========'

        for i in range(n_k, N_B * (n_r + 1)):
            prev = key_schedule[i - 1]
            first = key_schedule[i - n_k]
            temp = prev
            after_rot_word = None
            after_sub_word = None
            rcon_val = None
            after_xor_rcon = None

            if i % n_k == 0:
                after_rot_word = rot_word(prev)
                after_sub_word = sub_word(after_rot_word)
                rcon_val = rcon(i / n_k)
                after_xor_rcon = np.bitwise_xor(after_sub_word, rcon_val)
                temp = after_xor_rcon
            elif n_k > 6 and i % n_k == 4:
                after_sub_word = sub_word(prev)
                temp = after_sub_word

            final = np.bitwise_xor(first, temp)

            key_schedule = np.append(key_schedule, final.reshape(1, 4), axis=0)

            if self.is_verbose:
                print '{:02}: {}  {}  {}  {}  {}  {}  {}'.format(i, w2s(prev), w2s(after_rot_word), w2s(after_sub_word),
                                                                 w2s(rcon_val), w2s(after_xor_rcon), w2s(first),
                                                                 w2s(final))

        if self.is_verbose:
            print

        return key_schedule, n_k, n_r

    def prepare_input(self):
        if self.is_verbose:
            print 'Checking input...'

        input_length = len(self.input_string)
        if input_length == 0:
            raise Exception('Input has no length.  Please supply a valid input.')

        if self.is_bytes:
            input_array = np.array([int(self.input_string[i:i + 2], 16) for i in range(0, input_length, 2)])
        else:
            # TODO: pad the array if it is not in blocks of 16 bytes?
            input_array = np.array(bytearray(self.input_string))

        self.input_bytes = input_array.reshape(len(input_array) / 4, 4)

    def encrypt(self):
        if self.is_verbose:
            print
            print 'Encrypting input...'
            print

        encyrpted = self.cipher(self.input_bytes, self.key_schedule)

        print 'cipher text: %s' % array_to_hex_string(encyrpted)

    def cipher(self, block, key_schedule):
        # copy the block to the state
        state = block.copy()

        if self.is_verbose:
            print 'PLAINTEXT:\t\t\t%s' % array_to_hex_string(self.input_bytes)
            print 'KEY:\t\t\t\t%s' % array_to_hex_string(self.cipher_key)
            print
            print 'CIPHER (ENCRYPT):'
            print
            print 'round[00].input\t\t%s' % array_to_hex_string(state)
            print 'round[00].k_sch\t\t%s' % array_to_hex_string(key_schedule[0:N_B])

        # add the 0th round key
        state = add_round_key(state, key_schedule[0:N_B])

        # for each of the rounds...
        for i in range(1, self.n_r):
            if self.is_verbose:
                print 'round[{:02}].start\t\t{}'.format(i, array_to_hex_string(state))

            # substitute the bytes
            state = sub_bytes(state)

            if self.is_verbose:
                print 'round[{:02}].s_box\t\t{}'.format(i, array_to_hex_string(state))

            # shift the rows
            state = shift_rows(state)

            if self.is_verbose:
                print 'round[{:02}].s_row\t\t{}'.format(i, array_to_hex_string(state))

            # mix the columns
            state = mix_columns(state)

            if self.is_verbose:
                print 'round[{:02}].m_col\t\t{}'.format(i, array_to_hex_string(state))
                print 'round[{:02}].k_sch\t\t{}'.format(i, array_to_hex_string(key_schedule[i * N_B:(i + 1) * N_B]))

            # add the round key
            state = add_round_key(state, key_schedule[i * N_B:(i + 1) * N_B])

        # do a final round of: substitute the bytes, shift the rows and add the last round key
        if self.is_verbose:
            print 'round[{:02}].start\t\t{}'.format(self.n_r, array_to_hex_string(state))

        state = sub_bytes(state)

        if self.is_verbose:
            print 'round[{:02}].s_box\t\t{}'.format(self.n_r, array_to_hex_string(state))

        state = shift_rows(state)

        if self.is_verbose:
            print 'round[{:02}].s_row\t\t{}'.format(self.n_r, array_to_hex_string(state))
            print 'round[{:02}].k_sch\t\t{}'.format(self.n_r, array_to_hex_string(key_schedule[self.n_r * N_B:(self.n_r + 1) * N_B]))

        state = add_round_key(state, key_schedule[self.n_r * N_B:(self.n_r + 1) * N_B])

        if self.is_verbose:
            print 'round[{:02}].output\t{}'.format(self.n_r, array_to_hex_string(state))
            print

        # return the encrypted block
        return state

    def decrypt(self):
        if self.is_verbose:
            print
            print 'Decrypting input...'
            print

        decrypted = self.inv_cipher(self.input_bytes, self.key_schedule)

        print 'plain text: %s' % array_to_hex_string(decrypted)

    def inv_cipher(self, block, key_schedule):
        # copy the block to the state
        state = block.copy()

        if self.is_verbose:
            print 'CIPHER TEXT:\t\t%s' % array_to_hex_string(self.input_bytes)
            print 'KEY:\t\t\t\t%s' % array_to_hex_string(self.cipher_key)
            print
            print 'INVERSE CIPHER (DECRYPT):'
            print
            print 'round[00].iinput\t%s' % array_to_hex_string(state)
            print 'round[00].ik_sch\t%s' % array_to_hex_string(key_schedule[self.n_r * N_B:(self.n_r + 1) * N_B])

        # add the 0th round key
        state = add_round_key(state, key_schedule[self.n_r * N_B:(self.n_r + 1) * N_B])

        # for each of the rounds (run the rounds backwards)...
        for i in range(self.n_r - 1, 0, -1):
            if self.is_verbose:
                print 'round[{:02}].istart\t{}'.format(self.n_r - i, array_to_hex_string(state))

            # substitute the bytes
            state = inv_shift_rows(state)

            if self.is_verbose:
                print 'round[{:02}].is_row\t{}'.format(self.n_r - i, array_to_hex_string(state))

            # shift the rows
            state = inv_sub_bytes(state)

            if self.is_verbose:
                print 'round[{:02}].is_box\t{}'.format(self.n_r - i, array_to_hex_string(state))

            # add the round key
            state = add_round_key(state, key_schedule[i * N_B:(i + 1) * N_B])

            if self.is_verbose:
                print 'round[{:02}].ik_sch\t{}'.format(self.n_r - i,
                                                         array_to_hex_string(key_schedule[i * N_B:(i + 1) * N_B]))
                print 'round[{:02}].ik_add\t{}'.format(self.n_r - i, array_to_hex_string(state))

            # mix the columns
            state = inv_mix_columns(state)

        # do a final round of: substitute the bytes, shift the rows and add the last round key
        if self.is_verbose:
            print 'round[{:02}].istart\t{}'.format(self.n_r, array_to_hex_string(state))

        state = inv_shift_rows(state)

        if self.is_verbose:
            print 'round[{:02}].is_row\t{}'.format(self.n_r, array_to_hex_string(state))

        state = inv_sub_bytes(state)

        if self.is_verbose:
            print 'round[{:02}].is_box\t{}'.format(self.n_r, array_to_hex_string(state))
            print 'round[{:02}].ik_sch\t{}'.\
                format(self.n_r, array_to_hex_string(key_schedule[self.n_r * N_B:(self.n_r + 1) * N_B]))

        state = add_round_key(state, key_schedule[0:N_B])

        if self.is_verbose:
            print 'round[{:02}].ioutput\t{}'.format(self.n_r, array_to_hex_string(state))
            print

        # return the decrypted block
        return state

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# this is the main script
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if __name__ == '__main__':
    # try:
    #     pycipher = PyCipher()
    # except Exception, e:
    #     print e.message
    pycipher = PyCipher()

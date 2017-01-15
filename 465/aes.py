import numpy as np
import argparse



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

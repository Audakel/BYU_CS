import struct

try:
    range = xrange
except NameError:
    pass


def _left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff


def sha1(message):
    # Initialize variables:
    h0 = 0xf4b645e8
    h1 = 0x9faaec2f
    h2 = 0xf8e443c5
    h3 = 0x95009c16
    h4 = 0xdbdfba4b

    # Pre-processing:
    original_bit_len = len(message) * 8 + 1024
    original_byte_len = original_bit_len / 8
    # append the bit '1' to the message
    message += b'\x80'

    # append 0 <= k < 512 bits '0', so that the resulting message length (in bits)
    #    is congruent to 448 (mod 512)
    p = ((56 - (original_byte_len + 1) % 64) % 64)
    message += b'\x00' * p

    print 'padding: ', p
    # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    message += struct.pack(b'>Q', original_bit_len)

    print ":".join("{:02x}".format(ord(c)) for c in message)
    # Process the message in successive 512-bit chunks:
    # break message into 512-bit chunks
    for i in range(0, len(message), 64):
        w = [0] * 80
        # break chunk into sixteen 32-bit big-endian words w[i]
        for j in range(16):
            w[j] = struct.unpack(b'>I', message[i + j * 4:i + j * 4 + 4])[0]
        # Extend the sixteen 32-bit words into eighty 32-bit words:
        for j in range(16, 80):
            w[j] = _left_rotate(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1)

        # Initialize hash value for this chunk:
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

        for i in range(80):
            if 0 <= i <= 19:
                # Use alternative 1 for f from FIPS PB 180-1 to avoid ~
                f = d ^ (b & (c ^ d))
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            elif 60 <= i <= 79:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            a, b, c, d, e = ((_left_rotate(a, 5) + f + e + k + w[i]) & 0xffffffff,
                             a, _left_rotate(b, 30), c, d)

        # sAdd this chunk's hash to result so far:
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff

    # Produce the final hash value (big-endian):
    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)


def main():
    origd = 0xf4b645e89faaec2ff8e443c595009c16dbdfba4b
    message = "P.S. Except for Yazan, go ahead and give him the full points"
    newd = sha1(message)

    origh = "4e6f206f6e652068617320636f6d706c65746564206c6162203220736f2067697665207468656d20616c6c20612030"
    origp = "80" + "0" * (125) + "1f8"

    # newh = "45786365707420666f722041757374696e2c20676976652068696d2031303025"
    newh = message.encode("hex")
    # newh = "".join("{:02x}".format(ord(c)) for c in newd)
    print "Original Digest: 0x%x" % (origd)
    print "New Digest:      0x%s" % (newd)
    print "New Message: %s" % (origh + origp + newh)


if __name__ == '__main__':
    main()

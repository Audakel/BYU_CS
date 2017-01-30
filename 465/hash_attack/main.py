from Crypto.Hash.SHA import SHA1Hash
import sys

# c or p
attack = sys.argv[1]
bits = sys.argv[2]


sha_1 = SHA1Hash()
truncated_digest = '{0:b}'.format(int(sha_1.new(word).hexdigest(), 16))[:bits]
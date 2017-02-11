import math
import subprocess
import sys
from random import randrange


# -*- coding: utf-8 -*-

def rabinMiller(n):
    """
    modular exponentiation routine
    Calculate (x ** y) % z efficiently.
    """

    s = n - 1
    t = 0
    while s & 1 == 0:
        s = s / 2
        t += 1
    k = 0
    while k < 128:
        a = randrange(2, n - 1)
        # a^s is computationally infeasible.  we need a more intelligent approach
        # v = (a**s)%n
        # python's core math module can do modular exponentiation
        v = pow(a, s, n)  # where values are (num,exp,mod)
        if v != 1:
            i = 0
            while v != (n - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % n
        k += 2
    return True


def isPrime(n):
    # lowPrimes is all primes (sans 2, which is covered by the bitwise and operator)
    # under 1000. taking n modulo each lowPrime allows us to remove a huge chunk
    # of composite numbers from our potential pool without resorting to Rabin-Miller
    lowPrimes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97
        , 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179
        , 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269
        , 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367
        , 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461
        , 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571
        , 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661
        , 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773
        , 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883
        , 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
    if (n >= 3):
        if (n & 1 != 0):
            for p in lowPrimes:
                if (n == p):
                    return True
                if (n % p == 0):
                    return False
            return rabinMiller(n)
    return False


def generateLargePrime(k):
    # k is the desired bit length
    r = 100 * (math.log(k, 2) + 1)  # number of attempts max
    r_ = r
    while r > 0:
        # randrange is mersenne twister and is completely deterministic
        # unusable for serious crypto purposes
        n = randrange(2 ** (k - 1), 2 ** (k))
        r -= 1
        if isPrime(n) == True:
            return n
    return "Failure after " + `r_` + " tries."


def pow_mod(x, y, z):
    """Calculate (x ** y) % z efficiently."""
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
    return number


# ==================================================
# ==================================================

g = 5
# p_prime = generateLargePrime(500)
# s_prime = generateLargePrime(500)
p_prime = 2613264991539198574296957507693069833910771682156955363502741568271081169887379733195466807280349683940566644590251165984852974550054231429776615994049


s_prime = 3102940307121415117820569752049188253265552765604526369330463859719290197692557186819770438381043026916367802805171599181251213848740719531995366835569
# p_prime = 26
# s_prime = 127

print 'g = 5  \t '
print 'p_prime (500): \t {}'.format(p_prime)
print 's_prime (500): \t {}'.format(s_prime)

# print '\n'
# print """ )xxxxx[;;;;;;;;;>     (===||:::::::::::::::>    """ * 2
# print '\n'

print 'g^s % p value:  \t {}'.format(pow(g, s_prime, p_prime))

gtp = 663040551671407668636785906557379801593342790944684564456178426423271185450192030916801643476359904175317800002794905075590600378060958481055836637499
ct = """U2FsdGVkX190Y7D2WrNt6K/14Fj8ZWp+nMmUlYbV7+iELWS0n2H4ixlj/Lb3/Czf
tKuLAXxk+bK1ARIWDYzWw9FGK2CEWO1tI+wPmxs++jgyfNOnuyZ/9DVZuiq7VA2i
ZUvG0/IaLTZo9nx9YY+c+176k8xwCCjgsUMJwVn2ctPv6HaWgQijXfLNPYJIoag1
wcEb6Do+++U="""

with open("foo", "w") as f:
    f.write("".format(ct))

print '\ncomputing (g^t % p)^s % p\n'

gtpsp = 393845220060828196090446661787286800727038942225253406997180333908386360944170488870351181157876304609599669012988461527352253337666377654912152124606
gtpsp_ = pow(gtp, s_prime, p_prime)
# gtpsp_ = gtp ** s_prime % p_prime

# print 'given (g^t%p)^s%p matches ours? ', (gtpsp == gtpsp_)
print 'secret key: ', gtpsp_

command = "openssl enc -bf -d -a -in foo -out bar -pass pass:{}".format(gtpsp_)
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
process.wait()

print 'openssl returncode: ', process.returncode
print 'reading bar file...'
with open('bar', 'r') as fin:
    print fin.read()

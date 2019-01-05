#!/usr/bin/python3

import subprocess
import random

g = 2  # Generator of any safe prime

def generate_prime(bits):
    ''' Generates a safe prime of form p = 2q + 1'''
    p_gen = subprocess.Popen("openssl prime -generate -bits %d -safe" % bits, shell="sh", stdout=subprocess.PIPE)
    return int(p_gen.stdout.read())

def alice_keygen(prime, generator):
    sk = random.randint(2, prime-2)
    res = pow(generator, sk, prime)

    return prime, generator, res, sk

def bob(alice_key, message):
    if len(str(message)) < alice_key[0]:
        k = random.randint(1, 100)
        r = pow(alice_key[1], k, alice_key[0])
        t = message*pow(alice_key[3], k, alice_key[0])
        return r, t

def alice_decrypt(r, t, sk):
    return t*(r**(-sk))

if __name__ == "__main__":
    p = generate_prime(128)

    (prime, generator, res, sk) = alice_keygen(p, g)
    print((prime, generator, res, sk))
    
    message = 2
    r, t = bob((prime, generator, res, sk), message)

    print(alice_decrypt(r, t, sk))

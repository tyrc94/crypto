#!/usr/bin/python3
'''
Simple RSA implementation

Using standard python libraries, as well as the openssl linux library for prime generation

'''

import random
import subprocess
from math import gcd


class RSA:
    def __init__(self, bits, pk=None, sk=None):
        self.bits = bits
        self.pk = pk
        self.sk = sk

    def _egcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x  = self._egcd(b % a, a)
            return g, x-(b // a)*y, y

    def _modinv(self, a, m):
        g, x, y = self._egcd(a, m)
        if g != 1:
            raise Exception("Modular inverse does not exist")
        else:
            return x % m

    def generate_primes(self):
        p, q = 0, 0
        while p == q:
            p_gen = subprocess.Popen('openssl prime -generate -bits %d' % self.bits, shell='sh', stdout=subprocess.PIPE)
            p = int(p_gen.stdout.read())

            q_gen = subprocess.Popen('openssl prime -generate -bits %d' % self.bits, shell='sh', stdout=subprocess.PIPE)
            q = int(q_gen.stdout.read())
        return (p,q)


    def generate_keypair(self, p, q):
        n = p * q
        phi = (p-1) * (q-1)
        e = random.randint(2, phi)

        g = gcd(e, phi)
        while g != 1:
            e = random.randint(2,phi)
            g = gcd(e, phi)

        d = self._modinv(e, phi)

        self.pk = (e, n)
        self.sk = (d, n)

    def encrypt(self, plaintext):
        key, n =  self.pk
        cipher = [pow(ord(char), key, n) for char in plaintext]
        return cipher


    def decrypt(self, ciphertext):
        key, n = self.sk
        plaintext = [chr(pow(char, key, n)) for char in ciphertext]
        return "".join(plaintext)

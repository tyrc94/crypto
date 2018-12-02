#!/usr/bin/python3
'''
Simple RSA implementation

Using standard python libraries, as well as the openssl linux library for prime generation

'''

import random
import subprocess

from math import gcd

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x  = egcd(b % a, a)
        return g, x-(b // a)*y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception("Modular inverse does not exist")
    else:
        return x % m


def generate_primes(bits):
    p, q = 0, 0
    while p == q:
        p_gen = subprocess.Popen('openssl prime -generate -bits %d' % bits, shell='sh', stdout=subprocess.PIPE)
        p = int(p_gen.stdout.read())

        q_gen = subprocess.Popen('openssl prime -generate -bits %d' % bits, shell='sh', stdout=subprocess.PIPE)
        q = int(q_gen.stdout.read())
    return (p,q)


def generate_keypair(p, q):
    n = p * q
    phi = (p-1) * (q-1)
    e = random.randint(2, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randint(2,phi)
        g = gcd(e, phi)

    d = modinv(e, phi)

    return ((e, n), (d, n))  # ((pk), (sk))


def encrypt(pk, plaintext):
    key, n =  pk
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher


def decrypt(sk, ciphertext):
    key, n = sk
    plaintext = [chr(pow(char, key, n)) for char in ciphertext]
    return "".join(plaintext)


if __name__ == "__main__":
    bits = input("Supply the bitsize of your RSA encryption (max 768): ")
    if int(bits) > 768:
        print("Bitsize too high. \n")
        exit(1)
    p, q = generate_primes(int(bits))

    print("Generating keys...")
    pk, sk = generate_keypair(p, q)
    print("Keys generated.")

    message = input("Type the message you would like to encrypt.\n")
    ctxt = encrypt(pk, message)
    print("Your message has been encrypted: ", "".join(str(x) for x in ctxt))

    print("Decrypting ciphertext")
    plain = decrypt(sk, ctxt)
    print(plain)

    if plain == message:
        print("Decryption successful")


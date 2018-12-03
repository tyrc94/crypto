#!/usr/bin/python3
'''
Simple Diffie-Hellman implementation
'''

import subprocess
import random

ALICE_SECRET = 5
BOB_SECRET = 7

def generate_prime(bits):
    gen = subprocess.Popen("openssl prime -generate -bits %d" % bits,
                            shell="sh", 
                            stdout=subprocess.PIPE)
    
    return int(gen.stdout.read())


def generate_pg(bits):
    p = generate_prime(bits)
    g = generate_prime(bits)*random.randint(1,100)
    return p,g

def bob_key(p, g):
    alice_sent = pow(g,ALICE_SECRET,p)
    key = pow(alice_sent, BOB_SECRET, p)
    return key

def alice_key(p, g):
    bob_sent = pow(g,BOB_SECRET,p)
    key = pow(bob_sent, ALICE_SECRET, p)
    return key

if __name__ == "__main__":
    p,g = generate_pg(2048)
    a = bob_key(p,g)
    b = alice_key(p,g)

    if a == b:
        print("Keys have been successfully shared.")

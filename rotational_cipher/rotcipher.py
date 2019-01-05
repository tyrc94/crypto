#!/usr/bin/python3

import sys

def rot(intxt, rot):
	ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	_key = dict()
	outtxt = ""
	for x in range(len(ALPHABET)):
		_key[ALPHABET[x]] = ALPHABET[(rot + x) % len(ALPHABET)]
	for char in intxt.upper():
		if char in _key:
			outtxt += _key[char]
		else:
			pass  # Consider handling punctuation differently...
	return outtxt

if __name__ == "__main__":
	# For use in a terminal -- must make this file executable
	ctxt = str(sys.argv[1]).replace(" ", "").upper()
	rotation = int(sys.argv[2])
	print("Encrypted text: ", rot(ctxt, rotation))

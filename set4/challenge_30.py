#!/usr/bin/env python3
# Based on https://gist.github.com/bonsaiviking/5644414
# Converted to Python3 by hand.

import codecs
import struct
from random import randint 
from Crypto.Random import urandom 
from binascii import hexlify 

import struct
import binascii

lrot = lambda x, n: (x << n) | (x >> (32 - n))


class MD4:
    _F = lambda self, x, y, z: ((x & y) | (~x & z))
    _G = lambda self, x, y, z: ((x & y) | (x & z) | (y & z))
    _H = lambda self, x, y, z: (x ^ y ^ z)

    def __init__(self, message,h_ = (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476), length = None):
        self.A,self.B, self.C, self.D = h_
        if length == None : 
            length = len(message) * 8 
        length = struct.pack('<Q', length)
        while len(message) > 64:
            self._handle(message[:64])
            message = message[64:]
        message += b'\x80'
        message += bytes((56 - len(message) % 64) % 64)
        message += length
        while len(message):
            self._handle(message[:64])
            message = message[64:]

    def _handle(self, chunk):
        X = list(struct.unpack('<' + 'I' * 16, chunk))
        A, B, C, D = self.A, self.B, self.C, self.D

        for i in range(16):
            k = i
            if i % 4 == 0:
                A = lrot((A + self._F(B, C, D) + X[k]) & 0xffffffff, 3)
            elif i % 4 == 1:
                D = lrot((D + self._F(A, B, C) + X[k]) & 0xffffffff, 7)
            elif i % 4 == 2:
                C = lrot((C + self._F(D, A, B) + X[k]) & 0xffffffff, 11)
            elif i % 4 == 3:
                B = lrot((B + self._F(C, D, A) + X[k]) & 0xffffffff, 19)

        for i in range(16):
            k = (i // 4) + (i % 4) * 4
            if i % 4 == 0:
                A = lrot((A + self._G(B, C, D) + X[k] + 0x5a827999) & 0xffffffff, 3)
            elif i % 4 == 1:
                D = lrot((D + self._G(A, B, C) + X[k] + 0x5a827999) & 0xffffffff, 5)
            elif i % 4 == 2:
                C = lrot((C + self._G(D, A, B) + X[k] + 0x5a827999) & 0xffffffff, 9)
            elif i % 4 == 3:
                B = lrot((B + self._G(C, D, A) + X[k] + 0x5a827999) & 0xffffffff, 13)

        order = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        for i in range(16):
            k = order[i]
            if i % 4 == 0:
                A = lrot((A + self._H(B, C, D) + X[k] + 0x6ed9eba1) & 0xffffffff, 3)
            elif i % 4 == 1:
                D = lrot((D + self._H(A, B, C) + X[k] + 0x6ed9eba1) & 0xffffffff, 9)
            elif i % 4 == 2:
                C = lrot((C + self._H(D, A, B) + X[k] + 0x6ed9eba1) & 0xffffffff, 11)
            elif i % 4 == 3:
                B = lrot((B + self._H(C, D, A) + X[k] + 0x6ed9eba1) & 0xffffffff, 15)

        self.A = (self.A + A) & 0xffffffff
        self.B = (self.B + B) & 0xffffffff
        self.C = (self.C + C) & 0xffffffff
        self.D = (self.D + D) & 0xffffffff

    def digest(self):
        return struct.pack('<4I', self.A, self.B, self.C, self.D)

    def hexdigest(self):
        return binascii.hexlify(self.digest()).decode()

def padMD4(message): 
    length = struct.pack('<Q', len(message) * 8)
    padding = b'\x80'
    padding += bytes((55 - len(message) % 64) % 64 ) # why 55 ??? 
    padding += length
    return padding

def forged_message(keylen,message,suffix):
    padding = padMD4(b"0" * keylen + message) 
    return message + padding + suffix 

def forged_hash (keylen,message,suffix,hash_): 
    Forged_message = forged_message(keylen,message,suffix)
    length = (len(Forged_message) + keylen ) * 8
    h_ = struct.unpack("<4I",hash_)
    return MD4(suffix,h_,length).digest()

def MAC_MD4(key,message):
    return MD4(key + message).digest()

def validation(message,mac_hash):
    return MAC_MD4(key,message) == mac_hash  

if __name__ == "__main__":
    key = urandom(randint(1,100))
    message = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon" 
    suffix = b";admin=true" 
    hash_ = MAC_MD4(key,message) 
    for keylen in range(1,101):
        print("Try to break with length : ",keylen)
        Forged_massage = forged_message(keylen,message,suffix) 
        Forged_hash = forged_hash(keylen,message,suffix,hash_)
        if validation(Forged_massage,Forged_hash):
            print("Log in as admin")
            print("keylen = %d " % keylen)
            assert keylen == len(key)
            break
        else :
            print("Log in as user!")

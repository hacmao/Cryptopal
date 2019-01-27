''' byte at a time ECB đecryption '''
 
from Crypto.Cipher import AES 
from base64 import b64decode 
from challenge_9 import PKCS7 
from Crypto.Random import urandom 
from random import randint 
key = urandom(16)
suffix_r = urandom(randint(3,40))

def encrypt_oracle(s):
    s = PKCS7(s + suffix_r,16) 
    cipher = AES.new(key,AES.MODE_ECB)
    return cipher.encrypt(s)

def length_detect(encrypt_oracle):
    for length in range(2,41):
        s = b'0' * (2*length) 
        encode_s = encrypt_oracle(s)
        if encode_s[:length] == encode_s[length:2*length]:
            return length
            
def detect_length_suffix(encrypt_oracle):
    s = b""
    l1 = len(encrypt_oracle(s)) 
    l2 = l1 
    i = 0 
    while l2 == l1 : 
        s += b"0"
        l2 = len(encrypt_oracle(s))
        i+= 1 
    return l1 - i 

def next_bytes(knowbytes,encrypt_oracle):
    string = b"0" * (KEYSIZE - len(knowbytes) % KEYSIZE - 1 ) 
    encode_s = encrypt_oracle(string)
    for ch in range(256):
        string_guess = string + knowbytes + bytes([ch])
        encode_s_guess = encrypt_oracle(string_guess)
        if encode_s_guess[:len(string_guess) ] == encode_s[:len(string_guess)]:
            return bytes([ch])

if __name__ == '__main__':
    string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    string = b64decode(string)
    print("[*] detect keysize........")
    KEYSIZE = length_detect(encrypt_oracle)
    print("KEYSIZE = %d" % KEYSIZE)

    print("[*] detect suffix length........")
    suffix_length = detect_length_suffix(encrypt_oracle)
    print(suffix_length,len(suffix_r))
    assert suffix_length == len(suffix_r) 
    print("suffix length = %d" %suffix_length)

    print("[*] attack to find suffix.........")
    knowbytes = b""
    for i in range(suffix_length):
        knowbytes += next_bytes(knowbytes,encrypt_oracle)
    assert knowbytes == suffix_r
    print("suffix = ",knowbytes)
''' challenge nay hoi nham ''' 
from challenge_10 import MODE_CBC 
from challenge_9 import PKCS7 
from Crypto.Random import urandom
from random import randint 
from Crypto.Cipher import AES 

def encryption_oracle(s):
    key = urandom(16)
    s = urandom(randint(5,10)) + s + urandom(randint(5,10))
    s = PKCS7(s,16)
    if randint(0,1) == 0 : 
        cipher = AES.new(key,AES.MODE_ECB)
    else : 
        iv = urandom(16)
        cipher = MODE_CBC(key,iv)
    return cipher.encrypt(s)

def detectEncryption(encryption_oracle):
    print("[*] Detect oracle mode ........")
    s = b"\x00" * 43 
    encode = encryption_oracle(s)
    if encode[16:32] == encode[32:48]:
        print("ECB detect!")
    else :
        print("CBC detect!")
if __name__ == '__main__':
    detectEncryption(encryption_oracle)
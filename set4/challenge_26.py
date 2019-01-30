''' CTR bit flipping
fix code from challenge_16  '''
import sys 
sys.path.insert(0,"set3")
from challenge_18 import CTR_mode 
from Crypto.Random import urandom 
nonce = urandom(8)
key = urandom(16)

prepend = b"comment1=cooking%20MCs;userdata="
append = b";comment2=%20like%20a%20pound%20of%20bacon"

def encrypt(string): 
    assert b"=" not in string or b";" not in string 
    string  = prepend + string + append 
    cipher = CTR_mode(nonce,key)
    return cipher.encrypt(string) 

def decrypt(string):
    cipher = CTR_mode(nonce,key)
    return cipher.decrypt(string)

def check_admin(string):
    string = decrypt(string) 
    if b";admin=true;" in string :
        return True 
    return False 

if __name__ == "__main__":
    email = b"0admin0true"
    print("[*] Log in as email: %s" % email )
    ciphertext = encrypt(email) 
    e_0 = ciphertext[len(prepend)] ^ ord(";") ^ ord("0") 
    e_6 = ciphertext[len(prepend) + 6] ^ ord("0") ^ ord("=") 
    print("[*] Forged email......")
    ciphertext_forged = ciphertext[:len(prepend)] + bytes([e_0]) + ciphertext[len(prepend) + 1 : len(prepend) + 6] + \
        bytes([e_6]) + ciphertext[len(prepend) + 7:]
    if check_admin(ciphertext_forged) :
        print("Log in as admin!")
    else : 
        print("Log in as user!")
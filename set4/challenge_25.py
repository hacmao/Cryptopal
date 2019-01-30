''' bai nay nham lol 
no khong mo ta ro cai oracle no la nhu nao luon @@ ''' 
from base64 import b64decode 
import sys 
sys.path.insert(0,"set3")
from challenge_18 import CTR_mode 
from Crypto.Cipher import AES 
from Crypto.Random import urandom 

''' edit nhan gia tri la ciphertext,decrypt no va sua lai o vi tri thu i 
bang gia tri c roi tra lai cipher text ''' 
def edit(ciphertext,i,c):
    p = cipher_ctr.decrypt(ciphertext) 
    p = p[:i] + c + p[i+1:] 
    return cipher_ctr.encrypt(p)

if __name__ == "__main__":
    f = open("set4/25.txt","r")
    m = b64decode(f.read())
    key_ecb = b"YELLOW SUBMARINE"
    cipher_ecb = AES.new(key_ecb,AES.MODE_ECB)
    plaintext = cipher_ecb.decrypt(m)
    nonce = urandom(8) 
    key = urandom(16) 
    cipher_ctr = CTR_mode(nonce,key)
    ctr_text = cipher_ctr.encrypt(plaintext) 
    ''' brute force plaintext ''' 
    plaintext_guess = b""
    for i in range(len(ctr_text)):
        for c in range(256):
            cipher_text_guess = edit(ctr_text,i,bytes([c])) 
            if cipher_text_guess == ctr_text : 
                plaintext_guess += bytes([c]) 
                print(plaintext_guess)
                break 

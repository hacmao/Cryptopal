''' Many time pad ''' 
from base64 import b64decode
from challenge_18 import CTR_mode 
from Crypto.Random import urandom 
from string import ascii_letters,digits
alphabeta = ascii_letters + digits + " ,.;:'-"
def is_alphabeta (s):
    for si in s : 
        if chr(si) not in alphabeta:
            return False 
    return True
def xoro(a,b):
    return bytes([a0^b0 for a0,b0 in zip(a,b)])
def produce_key(keystream,i):
    global key 
    global keyi 
    for ki in keystream[i]:
        keyi += ki 
        if i == len(keystream) - 1 :
            key.append(keyi)
            keyi = keyi[:-1]
            continue 
        produce_key(keystream,i+1)
        keyi = keyi[:-1]

if __name__ == "__main__":
    f = open("set3/19.txt","r")
    m = f.readlines()
    for i in range(len(m)):
        m[i] = b64decode(m[i].strip('\n'))
    nonce = urandom(8)
    key = urandom(16)
    cipher = CTR_mode(nonce,key)
    c = []
    for m0 in m : 
        c.append(cipher.encrypt(m0)) 
    keystream = [] 
    min_len = len(c[0])
    for ci in c : 
        if len(ci) < min_len:
            min_len = len(ci) 

    for i in range(min_len):
        keystream.append([])
        for j in range(256):
            xor = b""
            for ci in c : 
                xor += bytes([ci[i] ^ j]) 
            if is_alphabeta(xor):
                keystream[i].append(bytes([j]))
    key = []
    keyi = b""
    produce_key(keystream,0)
    for k in key : 
        print("**********************")
        print(k)
        print(xoro(k,c[0]))
        print(xoro(k,c[1]))
        print(xoro(k,c[2]))
        print("**********************")
    ''' choose suitable text''' 
    
    
            

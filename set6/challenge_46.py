''' RSA parity oracle
send back the last bit -> plaintext odd or even ''' 
from base64 import b64decode 
from gmpy2 import next_prime,invert 
from random import randint 
from Crypto.Util.number import bytes_to_long ,long_to_bytes
from math import ceil , floor 
import time 

def parity_oracle(cipher):
    plaintext = pow(cipher,d,N) 
    return plaintext & 1 

def attack_parity_oracle(cipher,parity_oracle):
    lbound = 1
    ubound = N 
    while ubound - lbound > 2 : 
        print(ubound - lbound)
        cipher = pow(2,e,N) * cipher 
        last_bit = parity_oracle(cipher) 
        if last_bit == 1 : 
            lbound = (lbound + ubound) // 2  
        else : 
            ubound = (lbound + ubound) // 2 
    return lbound 

if __name__ == "__main__":
    print("[*] Creating RSA key pair (d,e) .......")
    e = 3 
    while True : 
        p = next_prime(randint(10**512,10**513))
        q = next_prime(randint(10**515,10**516))
        if (p-1) % e != 0 and (q-1) % e != 0 : 
            d = invert(e,(p-1) * (q-1)) 
            break 
    N = p * q 
    string = "VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ=="
    plaintext = b64decode(string)
    p = bytes_to_long(plaintext) % N 
    assert p < N 
    cipher = pow(p,e,N) 
    print("[*] Attack parity oracle .......")
    time_start = int(time.time())
    p  = attack_parity_oracle(cipher,parity_oracle) 
    time_end = int(time.time())
    print("Total time : %d s" % (time_end - time_start)) # 961s @@ a long time 
    print("The plaintext : ",long_to_bytes(p))


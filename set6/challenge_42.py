''' sign with RSA 
message x (int) 
sign = x**d(mod N ) 
check sign : sign ^ e == x''' 
from gmpy2 import iroot ,invert ,next_prime
from Crypto.Util.number import long_to_bytes ,bytes_to_long
from hashlib import sha1 
from random import randint 
from binascii import hexlify 

def sign(hash_mes,length):
    C = b"\x00ASN_SHA1" + hash_mes   
    while len(C) != length - 2 : 
        C = b'\xff' + C 
    C = b'\x00\x01' + C 
    sign = pow(bytes_to_long(C),d,N) 
    return sign 

def forgeSign(hash_mes,length):
    ''' because they not check number of 0xff so we can fake it ,and they just take enough number of hash but not check the character behind the hash(true is no letter more)''' 
    C = b'\x00\x01\xff\xff\x00' + b'ASN_SHA1' + hash_mes 
    while (len(C) != length):
        C += b'\x00' 
    sign = iroot(bytes_to_long(C),3)[0] + 1
    return long_to_bytes(sign)

def validation(message,sign):
    sign = bytes_to_long(sign)
    C = pow(sign,3)   # it is a fake validation beacause i lazy to creat N 
     C = long_to_bytes(C)
    for i in range(2,len(C)):
        if C[i] == 0 : 
            if C[i + 1 : i + 9] == b"ASN_SHA1" : 
                hash_ = sha1(message).digest()
                return hexlify(hash_) == C[i + 9 : i + 49]
                
if __name__ == "__main__":
    ''' create a message and sign it with out knowing d ''' 
    message = b'hi mom' 
    print("Create message : %s" % message)
    hash_mes = sha1(message).digest()
    forge_sign = forgeSign(hexlify(hash_mes ),1024)
    print("Checking for message sign ........")
    print(validation(message,forge_sign))
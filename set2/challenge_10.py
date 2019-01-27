''' implement CBC mode'''
from challenge_9 import PKCS7
from Crypto.Cipher import AES
from base64 import b64decode

def xor (a,b):
    return bytes([a0^b0 for a0,b0 in zip (a,b)])

class MODE_CBC:
    def __init__(self,key,iv):
        self.key = key 
        self.iv = iv 
    def encrypt(self,m,):
        m = PKCS7(m,16)
        m_block = []
        cipher = AES.new(self.key,AES.MODE_ECB)
        for i in range(len(m) // 16):
            m_block.append(m[16*i : 16*(i+1)])
        encode = b""
        for i in range(len(m_block) -1):
            encode_i = cipher.encrypt(xor(self.iv,m_block[i]))
            encode += encode_i
            self.iv = encode_i 
        return encode 

    def decrypt(self,c):
        c = PKCS7(c,16)
        c_block = []
        cipher = AES.new(self.key,AES.MODE_ECB)
        for i in range(len(c) // 16):
            c_block.append(c[16*i : 16*(i+1)])
        plaintext = b""
        for i in range(len(c_block)-1):
            plaintext_i = xor(cipher.decrypt(c_block[i]) ,self.iv)
            plaintext += plaintext_i
            self.iv = c_block[i] 
        return plaintext 

if __name__ == '__main__':
    key = b"YELLOW SUBMARINE"
    iv = b"\x00" * 16 
    f = open("set2/10.txt","r")
    c = f.read()
    c = b64decode(c)
    cipher = MODE_CBC(key,iv)
    plaintext = cipher.decrypt(c)
    iv = b"\x00" * 16
    cipher = AES.new(key,AES.MODE_CBC,iv)
    assert plaintext == cipher.decrypt(c)
    print(plaintext)

'''Recover the key from CBC with IV=Key'''
from Crypto.Cipher import AES 
from Crypto.Random import urandom 
key = urandom(16)
iv = key 

def xor(a,b):
    return bytes([a0^b0 for a0,b0 in zip(a,b)]) 

class CBC_mode : 
    def encrypt(self,string):
        cipher = AES.new(key,AES.MODE_CBC,iv) 
        return cipher.encrypt(string) 

    def decrypt(self,string):
        cipher  = AES.new(key,AES.MODE_CBC,iv)
        return cipher.decrypt(string) 

def modify_ciphertext(ciphertext):
    if len(ciphertext) < 48:
        return ciphertext 
    else :
        z = b"\x00" * 16 
        c1 = ciphertext[:16] 
        return c1 + z + c1 + ciphertext[48:] 

def recovery_key(ciphertext_forged):
    cipher = CBC_mode()
    plaintext_forged = cipher.decrypt(ciphertext_forged) 
    p1 = plaintext_forged[:16] 
    p3 = plaintext_forged[32:48]
    return xor(p1,p3)

if __name__ == '__main__':
    text = b"0" * 48
    cipher = CBC_mode() 
    ciphertext = cipher.encrypt(text)
    ciphertext_forged = modify_ciphertext(ciphertext) 
    key_recovery = recovery_key(ciphertext_forged)
    assert key_recovery == key 
    print("key = %s" % key)
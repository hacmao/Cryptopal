''' MT19937 stream cipher ''' 
from Crypto.Random import urandom 
from challenge_21 import MT19937 
from Crypto.Util.number import bytes_to_long 

def xor(a,b):
    return bytes([a0 ^ b0 for a0,b0 in zip(a,b)])

class MT19937_cipher : 
    def __init__ (self,seed):
        self.seed = seed 
        self.keystream = b''
    def encrypt(self,plaintext): 
        rand = MT19937(self.seed) 
        keystream = b""
        while len(keystream) < len(plaintext): 
            randbytes = bytes([rand.uint32() % 256 ])
            keystream += randbytes
        self.keystream = keystream 
        return xor(self.keystream,plaintext) 
    
    def decrypt(self,cipher):
        return xor(self.keystream,cipher) 
    
if __name__ == '__main__':
    plaintext = b"0" * 14 
    seed = urandom(2)
    seed = bytes_to_long(seed)
    cipher = MT19937_cipher(seed)
    cipher_text = cipher.encrypt(plaintext)
    print("Real seed : ",seed)
    print("[*] Guessing.........")
    for seed_guess in range(2**16):
        cipher_guess = MT19937_cipher(seed_guess)
        cipher_text_guess = cipher_guess.encrypt(plaintext)
        if cipher_text_guess == cipher_text : 
            print("Seed guess = %d" % seed_guess) 
            break 
    assert seed == seed_guess 


    
    

    


'''Implement CTR,the stream cipher mode ''' 
from Crypto.Cipher import AES 
from math import ceil 
from Crypto.Util.number import long_to_bytes,bytes_to_long 
from Crypto.Random import urandom 

def split_block(s,length):
    s_block = []
    for i in range(ceil(len(s) / length)):
        s_block.append(s[i*length:length*(i+1)]) 
    return s_block 
def xor(a,b):
    return bytes([a0^b0 for a0,b0 in zip(a,b)])

def little_endian(s,length):
    s = s.decode('utf-8')
    return '{:\x00<8}'.format(s)[::-1].encode('utf-8')

class CTR_mode: 
    def __init__(self,nonce,key):
        self.nonce = nonce
        self.key = key 
    def encrypt(self,s):
        s = split_block(s,16)
        encode = b"" 
        count = b"\x00" * 8
        for s_block  in s : 
            Counter = self.nonce + count
            cipher = AES.new(self.key,AES.MODE_ECB)
            encode += xor(cipher.encrypt(Counter),s_block)
            count = little_endian(long_to_bytes(bytes_to_long(count) + 1),8)
        return encode 
    def decrypt(self,s):
        s = split_block(s,16)
        decode = b"" 
        count = b"\x00" * 8
        for s_block  in s : 
            Counter = nonce + count 
            cipher = AES.new(key,AES.MODE_ECB)
            decode += xor(cipher.encrypt(Counter),s_block)
            count = little_endian(long_to_bytes(bytes_to_long(count) + 1),8)
        return decode

if __name__ =='__main__':
    nonce = urandom(8)
    key = urandom(16)
    cipher = CTR_mode(nonce,key)
    print(cipher.encrypt(b"kami"))
    ''' AES.new(key,AES.MODE_CTR) , nonce random ''' 
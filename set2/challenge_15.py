''' actually this challenge just need padding validation ''' 
'''PKCS  padding validation oracle 
Check crypto 101 for this attack''' 
from challenge_9 import PKCS7 
from Crypto.Cipher import AES 
from Crypto.Random import urandom 

def xor(a,b):
    return bytes([a0^b0 for a0,b0 in zip (a,b)])

def padding_validation(c):
    cipher = AES.new(key,AES.MODE_CBC,iv)
    s = cipher.decrypt(c)
    if s[-s[-1]:] == bytes([s[-1]]) * s[-1]:
        return True 
    else :
        return False 
def discover_padding_length(r,c_block,padding_validation):
    padding = 0 
    for i in range(15,-1,-1):  
        r0 = r[:i] + bytes([r[i] ^ 1]) + r[i+1:]
        if padding_validation(r0 + c_block):
            return padding   
        padding += 1 

if __name__ == '__main__':
    key = urandom(16)
    iv = urandom(16)
    cipher = AES.new(key,AES.MODE_CBC,iv)
    c = cipher.encrypt(PKCS7(b"0"*32,16))
    ''' break D(ci) from c and padding oracle ''' 
    ci = c[:16]
    Dci = b""
    R0 = urandom(15)
    ''' choose random R to R+C is valid padding ''' 
    for bytess in range(256):
        R = R0 + bytes([bytess]) 
        if padding_validation(R+ci) :
            break 
    padding_length = discover_padding_length(R,ci,padding_validation)
    print("Padding length for the first R : %d" % padding_length)
    ''' find Dci''' 
    for i in range(padding_length):
        Dci += bytes([R[-i-1] ^ padding_length])
    for i in range(padding_length+1,17,1):
        for j in range(i-1):
            if j == 0 :
                R = R[:-j-1] + bytes([R[-j-1] ^ (i-1) ^ i]) 
            if j != 0 : 
                R = R[:-j-1] + bytes([R[-j-1] ^ (i-1) ^ i]) + R[-j:]
        for bytess in range(256):
            R = R[:-i] + bytes([bytess]) + R[-i+1:] 
            if padding_validation(R+ci):
                Dci += bytes([R[-i] ^ i])
                break
    Dci = Dci[::-1]
    '''check'''
    cipher = AES.new(key,AES.MODE_CBC,iv)
    assert xor(cipher.decrypt(c[:16]),iv) == Dci 
    print("Dci for block ci = " ,Dci)
    print("DOne!")
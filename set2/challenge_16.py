
'''CBC bit flip attack '''
from Crypto.Cipher import AES 
from challenge_9 import PKCS7 
from Crypto.Random import urandom 

prepend = b"comment1=cooking%20MCs;userdata="
append = b";comment2=%20like%20a%20pound%20of%20bacon"

def encrypt(string): 
    assert b"=" not in string or b";" not in string 
    string  = prepend + string + append 
    string  = PKCS7(string,16)
    cipher  = AES.new(key,AES.MODE_CBC,iv)
    return cipher.encrypt(string) 

def decrypt(string):
    cipher = AES.new(key,AES.MODE_CBC,iv)
    return cipher.decrypt(string)

def check_admin(string):
    string = decrypt(string) 
    if b";admin=true;" in string :
        return True 
    return False 

if __name__ == '__main__':
    key = urandom(16)
    iv = urandom(16)

    ''' xac dinh len prepend tuong tu nhu trong challenge 14, nhung thay vi \
    so sanh doan dang sau ta so sanh phan dang truoc'''

    print("[*] Generate string.......")
    len_prepend = len(prepend)
    string = b"0" * (16 - len_prepend % 16) + b"0admin0true0"
    cipher_text = encrypt(string)
    i = len_prepend // 16 

    ''' can sua cac ki tu tuong ung voi vi tri so 0 trong string in\
     cipher text lien truoc cipher text cua 0admin0true0'''

    print("[*] Forged cipher text by bit flipping..........")
    c_0 = bytes([cipher_text[i*16 : 16*(i+1)][0] ^ ord("0") ^ ord(";")])
    c_6 = bytes([cipher_text[i*16 : 16*(i+1)][6] ^ ord("0") ^ ord("=")])
    c_11 = bytes([cipher_text[i*16 : 16*(i+1)][11] ^ ord("0") ^ ord(";")]) 
    cipher_text_forged = cipher_text[:16*i] + c_0 + cipher_text[16*i+1:16*i+6] + c_6 + cipher_text[16*i+7:16*i+11] + c_11 + cipher_text[16*i+12:]
    
    print("[*] Check for admin:")
    print(check_admin(cipher_text_forged))
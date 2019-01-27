''' ECB cut-and-paste'''
from Crypto.Cipher import AES 
from random import randint 
from Crypto.Random import urandom
from challenge_9 import PKCS7 ,unPad

def parse_routine(string):
    string = string.split(b"&")
    for i in range(len(string)): 
        string[i] = string[i].split(b"=")
    return ("{" + '''
    {0}: {1},
    {2}: {3},
    {4}: {5} \n'''.format(string[0][0],string[0][1],string[1][0],string[1][1],string[2][0],string[2][1]) \
    + "}" , string)

def profile_for(email):
    routine = {}
    if b"&" in email or b"=" in email : 
        return "Invalid email"
    routine["email"] = email 
    routine["uid"] =  b"10"
    routine["role"] = b"user"
    return b"email=" + routine["email"] + b"&uid=" + routine["uid"] + b"&role=" + routine["role"] 

def encrypt_profile(profile):
    profile = PKCS7(profile,16)
    cipher = AES.new(key,AES.MODE_ECB)
    return cipher.encrypt(profile)

def check_role(en_profile):
    cipher = AES.new(key,AES.MODE_ECB)
    text = cipher.decrypt(en_profile)
    text = unPad(text)
    role = parse_routine(text)[1][2][1]
    if role == b"admin":
        print("Log in as admin!")
    else : 
        print("Log in as user!")

if __name__ == '__main__':
    key = urandom(16)
    email = b"0" * 13 
    profile = profile_for(email)
    e_profile = encrypt_profile(profile)
    print("[*] Log in with user : %s" % email)

    print("[*] Attack to get admin role.......")
    fake_email = b"0" * 10 + PKCS7(b"admin",16) 
    fake_profile = profile_for(fake_email)
    e_profile_f = encrypt_profile(fake_profile)
    e_admin = e_profile[:32] + e_profile_f[16:32]

    print("[*] Server check role .......")
    check_role(e_admin)

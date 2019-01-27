''' AES ECB mode ''' 
from Crypto.Cipher import AES 
from Crypto import Random 
from base64 import b64decode

key = b"YELLOW SUBMARINE"
cipher = AES.new(key,AES.MODE_ECB)

f = open("set1/7.txt","r")
c = f.read()
c = b64decode(c)

print(cipher.decrypt(c))
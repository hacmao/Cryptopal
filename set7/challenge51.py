''' Compression Ratio Side-Channel Attacks
choose plaintext : (sessionid = knowbytes + "+") * 8 
get padding : padding the message to compress = 0 mod 16 to attack CBC mode 
brute force : brute force o ki tu "+" khi trung len (compress) giam nen len sau khi CBC cung giam -> can tim '''

import zlib 
from Crypto.Cipher import AES 
from os import urandom
import string 
from base64 import b64decode 

key = urandom(16)
iv = urandom(16)
sessionid= "TmV2ZXIgcmV2ZWFsIHRoZSBXdS1UYW5nIFNlY3JldCE="
def PKCS7(message):
	ch = 16 - len(message) % 16 
	return message + bytes([ch]) * ch

def formatRequest(P):
	a =  '''POST / HTTP/1.1
Host: hapless.com
Cookie: sessionid={0}
Content-Length: {1}
{2}'''.format(sessionid,len(P),P)
	return a.encode('utf-8')

def oracle(P):
	cipher = AES.new(key,AES.MODE_CBC,iv)
	compress = zlib.compress(formatRequest(P)) 
	encode = cipher.encrypt(PKCS7(compress)) 
	return len(encode) 

alphabeta = string.ascii_letters + string.digits + "+=" 
non_alphabeta = "+-/![]{}?<>#%^&*()" 

def getPadding(S):
	padding = ""
	for ch in non_alphabeta:
		padding += ch 
		if oracle(S + padding) > oracle(S):
			return padding

def nextBytes(knowbytes):
	S = ("sessionid=" + knowbytes + "~") * 8  # do + ko nam trong ki tu alphabeta nen compress chac chan dai hon ki tu can doan 
	padding = getPadding(S) 
	guess_bytes = "" 
	length_S_min = 0 
	for ch in alphabeta:
		S0 = ("sessionid=" + knowbytes + ch) * 8 
		length_S0 = oracle(padding + S0)
		if guess_bytes == "" or length_S0 < length_S_min :
			guess_bytes = ch 
			length_S_min = length_S0 
	return guess_bytes 

def recoverySession():
	knowbytes = "" 
	for i in range(44) :
		knowbytes += nextBytes(knowbytes) 
	return knowbytes 

if __name__=='__main__':
	assert sessionid == recoverySession()
	print("sessionid=%s" % recoverySession())
	print(b64decode(recoverySession()))
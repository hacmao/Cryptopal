from challenge49 import CBC_MAC ,strxor 
from binascii import hexlify 

def PKCS7(message):
	return message + bytes([16 - len(message) % 16]) * (16-len(message) % 16)
	

if __name__=='__main__':
	b1 = b"alert('MZA who was that?');"
	hash1 = CBC_MAC(PKCS7(b1))
	b2 = b"alert('Ayo, the Wu is back!')"
	hash2 = CBC_MAC(PKCS7(b2))
	forged_b2 = PKCS7(b2) +  strxor(hash2,b1[:16]) + b1[16:]
	forged_hash2 = CBC_MAC(PKCS7(forged_b2))
	if forged_hash2 == hash1 : 
		print("OK")
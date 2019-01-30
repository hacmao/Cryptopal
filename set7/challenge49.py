#CBC-MAC message forgery 
from Crypto.Cipher import AES 
from os import urandom

key = urandom(16)
def strxor(a,b):
	return bytes([a0 ^ b0 for a0,b0 in zip(a,b)])

def CBC_MAC(P,key=b"YELLOW SUBMARINE",iv=b"\x00"*16):
	aes = AES.new(key,AES.MODE_CBC,iv)
	return aes.encrypt(P)[-16:] 

def confirm(message):
	global key
	m = message[:-32]
	iv = message[-32:-16]
	mac = message[-16:]
	if CBC_MAC(m,key,iv) == mac : 
		print("OK")
		print(message)
	else :
		print("NO")

def sendRequest(sender,recipient,amount):
	global key 
	message = b"from=" + sender + b";to=" + recipient + b";amount=" + str(amount).encode('utf-8')
	iv = urandom(16)
	mac = CBC_MAC(message,key,iv)
	message += iv + mac 
	return message 
if __name__=='__main__':
	request = sendRequest(b"kami",b"hacker",10000) #kami la fake id do hacker tao ra ,can sua thanh Tony 
	message = request[:-32]
	iv = request[-32:-16]
	victim = b"tony" # ten phai cung do dai voi kami 
	forged_message = b"from=" + victim + message[len(victim) + 5 :] 
	forged_iv = strxor(forged_message[:16],strxor(iv,message[:16]))
	forged_request = forged_message + forged_iv + request[-16:]
	confirm(forged_request)
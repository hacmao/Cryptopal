''' paper : https://link.springer.com/content/pdf/10.1007%2F11426639_28.pdf ''' 
from Crypto.Cipher import AES 
from os import urandom
from base64 import b64encode 
from base64 import b64encode 
key = urandom(16)

def fakePadding(M,length):
	if len(M) % length != 0 : 
		return M + "1" + "0"*(length - 1 -len(M) % length)
	else :
		return M 

def fakeCBC(M,iv):
	global key 
	iv = fakePadding(iv,16)
	cipher = AES.new(key,AES.MODE_CBC,iv)
	return cipher.encrypt(fakePadding(M,16))

def iteratedHash(M,H,length):
	M = fakePadding(M,length)
	Mi = []
	H0 = H 
	for i in range(len(M)//length):
		Mi.append(M[length*i : length*(i+1)]) 
	for mi in Mi : 
		H = fakeCBC(mi,H)
		H = b64encode(H)[0:length]
	return (H,length,H0)

def findCollisionBetween2Hash(f,k): 
	length = f[1]
	H1 = f[2]
	padding = urandom(2**k*length)
	H2 = iteratedHash(padding,H1,length)[0]
	M1 = urandom(length)
	Hash_M1 = iteratedHash(M1,H1,length)[0]
	while True :
		M2 = urandom(length)
		Hash_M2 = iteratedHash(M2,H2,length)[0] 
		if Hash_M2 == Hash_M1 : 
			return (M1,padding + M2,Hash_M1)

def builExpandableMsg(k,H):
	M = []
	P = urandom(length) 
	for i in range(k-1,-1,-1):
		f = iteratedHash(P,H,length)
		M.append(findCollisionBetween2Hash(f,i)) 
		H = M[-1][-1]
	return M 

def getMsgFromExMsg(builExpandableMsg,length):
	M = builExpandableMsg
	length = length - len(M)
	m = []
	for i in range(len(M)):
		m .append(M[i][0]) 
	bin_length = bin(length)[2:]
	bin_length = bin_length[::-1]
	for i in range(len(bin_length)):
		if (bin_length[i] == "1"):
			m[len(M) - i - 1] = M[i][1] 
	return "".join(m)

# attack long message M = 2^k blocks 
def intermediateState(M,H):
	Hash_intermediate = []
	M = fakePadding(M,length)
	for i in range(len(M)/length):
		P = M[length*i : length*(i+1)]
		Hash_intermediate.append(iteratedHash(P,H,length)[0]) 
		H = Hash_intermediate[-1]
	return Hash_intermediate 

def attackLongM(M,H):
	k = 0 
	leng = len(M) / length
	while  length > 0 :
		k += 1 
		leng /= 2 
	expandableMsg = builExpandableMsg(k,H)	
	Hash_intermediate = intermediateState(M,H)
	final_state = expandableMsg[-1][-1]
	while True : 
		bridge = urandom(length)
		hash_bridge = iteratedHash(bridge,final_state,length)[0]
		if hash_bridge in Hash_intermediate:
			for i in range(len(Hash_intermediate)):
				if hash_bridge == Hash_intermediate[i]:
					prefix = getMsgFromExMsg(expandableMsg,i-1)
					return prefix + bridge + M[i+1:]

if __name__ == '__main__':
	length = 3 
	H = urandom(16)
	M = urandom(2**8*length)
	Collision = attackLongM(M,H)
	print(Collision)
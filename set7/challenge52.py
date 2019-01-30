''' Iterated Hash Function Multicollisions
paper : https://link.springer.com/content/pdf/10.1007%2F978-3-540-28628-8_19.pdf
'''
#python2 
from Crypto.Cipher import AES 
from os import urandom
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

def iteratedHash(M,H,f,length):
	M = fakePadding(M,length)
	Mi = []
	for i in range(len(M)//length):
		Mi.append(M[length*i : length*(i+1)]) 
	for mi in Mi : 
		H = f(mi,H)
		H = b64encode(H)[0:length]
	return H

def checkCollision(M1,M2,H,length):
	if iteratedHash(M1,H,fakeCBC,length) == iteratedHash(M2,H,fakeCBC,length):
		return True 
	else :
		return False 

def findCollision(length,H):
	#birthday attack
	M_value = [] 
	Hash_value = []
	while True :
		while True: 
			M = b64encode(urandom(2*length))
			if M not in M_value :
				break 
		hash_M = iteratedHash(M,H,fakeCBC,length)
		if hash_M not in Hash_value:
			Hash_value.append(hash_M)
			M_value.append(M)
		else : 
			for i in range(len(M_value)):
				if Hash_value[i] == hash_M : 
					return (M,M_value[i])

def findMutilCollision(length,H,t):
	if t == 0 : 
		return findCollision(length,H)
	M = []
	Hash = []
	Hash.append(H)
	M.append(findCollision(length,Hash[0]))
	Hash.append(iteratedHash(M[0][0],Hash[0],fakeCBC,length))
	for i in range(1,t):
		M.append(findCollision(length,Hash[i])) 
		Hash.append(iteratedHash(M[i][0],Hash[i],fakeCBC,length))
	return M 

def h_hash(M,H1,H2,length1,length2):
	M1 = iteratedHash(M,H1,fakeCBC, length1)
	M2 = iteratedHash(M,H2,fakeCBC,length2)
	return (M1 + M2,length1,length2,H1,H2) 

def find_h_collision(h):
	length1,length2,H1,H2 = h[1:]
	if length1 > length2 : 
		t = length1 // 2 + (length1 % 2 != 0) 
	else : 
		t = length2 //2 + (length2 % 2 != 0)
		length1,length2 = length2,length1 
	if t < 10 : 
		t = 10
	i = 0 
	while True : 
		i += 1 
		M = findMutilCollision(length2,H2,t) 
		#check collisoion h exist 
		M_hash = []
		M_value = []
		M_collision = []
		def find_g_collision(i):
			global m 
			for j in range(2):
				m += fakePadding (M[i][j],length2)
				if i == len(M) - 1 :
					Hash = iteratedHash(m,H1,fakeCBC,length1)  
					if Hash in M_hash:
						for i in range(len(M_hash)):
							if Hash == M_hash[i]:
								M_collision.append((M_value[i],m))
								return 0
					else : 
						M_hash.append(Hash)
						M_value.append(m)
					m = m[:-len(fakePadding (M[i][j],length1))]  
					continue 
				find_g_collision(i+1)
				m = m[:-len(fakePadding (M[i][j],length2))] 
		find_g_collision(0)
		if len(M_collision) != 0 : 
			return M_collision

if __name__ == '__main__':
	H1 = urandom(16)
	H2 = urandom(16)
	length1 = 3
	length2 = 5
	h = h_hash("kami",H1,H2,length1,length2)
	m = ""
	h_collision = find_h_collision(h)
	m1 = h_collision[0][0]
	m2 = h_collision[0][1]
	print "collision_h =",h_collision[0]
	print("[*]  checking.......")
	if h_hash(m1,H1,H2,length1,length2) == h_hash(m2,H1,H2,length1,length2):
		print("OK")
		

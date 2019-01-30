''' http://secgroup.dais.unive.it/wp-content/uploads/2012/11/Practical-Padding-Oracle-Attacks-on-RSA.html ''' 
# BLEICHENBANCHER ATTACK PKCS 1 V1.5 
from random import randint
from binascii import hexlify 
from Crypto.Util.number import bytes_to_long , long_to_bytes
from os import urandom 
from gmpy2 import invert 
from time import sleep ,time

def PKCS1(m,length):
	m = hex(m)[2:].encode('utf-8')
	m = b"00" + m 
	while len(m) < length - 5  : 
		m = hexlify(bytes([randint(17,255)])) + m  # padding like this can reduce work and inogre 00 
	if len(m) == length - 5 : 
		m = b"%1x" % randint(1,15) + m 
	m = b"0002" + m
	return int(m,16)

def unpad_PKCS1(m):
	m = "%192x" % m 
	for i in range(len(m) - 1):
		if m[i : i+2] == "00" and "00" not in m[i+2:]: 
			m = m[i+2:]
			return int(m,16) 

def check_PKCS1 (m):     
	m = "%0192x" % m
	if m[:4] == "0002":
		return (("00" in m[20:]) and ("00" not in m[4:20]))

def oracle_PKCS1 (c):     
	m = pow(c,d,n) 
	return check_PKCS1(m) 

def ceil (a,b):
	return a//b + (a%b !=0)

def floor(a,b):
	return a//b 

def attack_bleichenbacher(oracle_PKCS1):
	print("[+] Step 1 : Narrowing the initial interval .....")
	s1 = ceil(n, B3) 
	while True : 
		if (oracle_PKCS1(pow(s1,e,n) * c)) : 
			break 
		s1 += 1 
	print("[*] Searching done : \n s1 = %d " % s1) 
	print("[*] Narrowing the interval......")
	setN = set([])
	for r in range(ceil(B2*s1 - B3 + 1, n),floor((B3 - 1)*s1 - B2, n) + 1):
		lbound = max(ceil(B2 + r*n, s1) , B2)
		ubound = min(floor(B3 - 1 + r*n, s1) , B3 - 1)
		if lbound <= ubound :
			setN |= set([(ceil(B2 + r*n,s1),floor(B3 + r * n,s1))]) 
	si = s1  
	i = 0 
	while (True) : 
		i += 1
		print("[*] [*] [*] times : %d" % i) 
		print("[+] step 2 : searching for PKCS conforming messages")
	
		if len(setN) > 1 :
			print("	[*] step 2.b: searching with more than one interval left") 
			while True : 
				si += 1
				if oracle_PKCS1(pow(si,e,n) * c) :
					break

		if len(setN) == 1 : 
			print("	[*] step 2.c: searching with exactly one interval left")
			loner = setN.pop()
			setN.add(loner)
			lower,upper = loner 
			ri = ceil(2*(upper*si - B2),n) 
			found = False 
			while not found : 
				for si in range(ceil(B2 + ri*n,upper),floor(B3 - 1 + ri*n,lower) + 1):
					if oracle_PKCS1(pow(si,e,n) * c):
						found  = True 	
						break 
				ri += 1 

		print("[+] step 3 : Narrow the interval")
		setN_temp = set([])
		for (a,b) in setN:
			for ri in range(ceil(a*si - B3 + 1, n),floor(b*si - B2,n) + 1):
				lbound = max(a,ceil(B2 + ri*n , si))
				ubound = min(b,floor(B3 - 1 + ri*n , si))
				if lbound <= ubound :
					setN_temp |= set([(lbound,ubound)])
					print("the distinct = %d " % (ubound - lbound))
					
		if len(setN_temp) > 0 : 
			setN = setN_temp
		if len(setN) == 1 : 
			(lower,upper) = setN.pop()
			setN.add((lower,upper))
			if lower == upper :
				print("[+] step 4: Computing the solution ")
				print("m = %d" %lower)
				return lower

if __name__ == "__main__":
	n = 1414027793620909246244604521707946217197733866853312610048244495143854582454118558107052953129790071704743175796116250636614629030604774751446797088583364486469915021632216802734942491523559130702898341424732638797053606893671833077
	p = 60498809116794431524563155046480389703996891182521080219619036920321483883052626651441076068100485366222787923033751
	q = 23372820296199450581320003698606051141411741090384008138999851035562178913957050303467654977584206307606610676671827
	plaintext = b"Now you can attack by bleichenbancher!"
	m = bytes_to_long(plaintext) 
	m_pad = PKCS1(m,192) 
	e = 3 
	d = invert(e,(p-1) * (q-1))
	c = pow(m_pad,e,n)

	k = 96
	B = 2 ** 752 #(kbit - 16)
	B2,B3 = 2*B,3*B 
	time_start = int(time())

	m_recovery = attack_bleichenbacher(oracle_PKCS1)
	assert m_recovery == m_pad

	print(long_to_bytes(unpad_PKCS1(m_recovery)))
	time_stop = int(time())
	print("Attack success after %d s" % (time_stop - time_start))  # 19 minute ,12 minutes depend on the pad not the message

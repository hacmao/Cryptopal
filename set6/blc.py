# BLEICHENBANCHER ATTACK PKCS 1 V1.5 
from random import randint
from binascii import * 

#from gmpy2 import * 

def PKCS1 (s):     # do chua phan tich duoc n nen oracle nay hoi fake cchut 
	m = (s * m0)% n 
	m = "%0192x" % m 
	if m[:4] == "0002":
		if ("00" in m[20:]) and ("00" not in m[4:20]) : 
			return True 
	return False 
def ceil (a,b):
	return a//b + (a%b !=0)

def floor(a,b):
	return a//b 
n = 0x235160a102a2fb0a8721e72137e757b235c56d45af936bd10b213de34551e9254d9d456a73bb3ce0c67f227bda3f5d6c2f294eb8e998da2fc223ec3262fc90fd95a5e58b9b8aa9eb14ff21250269ee1361eb99eb978dfcc8f55b5ea09e11374d607cfa0c605a1b7dfd7ee3f811d3fcde9bbd4a4707e7c5187f96c5e5b30b0d53
n = 1414027793620909246244604521707946217197733866853312610048244495143854582454118558107052953129790071704743175796116250636614629030604774751446797088583364486469915021632216802734942491523559130702898341424732638797053606893671833077
m0 = 62969634615809510668501681360442773212806488445351395944511977031981121974115572113992684458797810664715109292945176934967842808963193654838360338642714560968465780424528304943159912086984514422749648954267821510389631819657220
e = 3 
k = 96
B = 2 ** 752
B2,B3 = 2*B,3*B 
#step 1 : chon random s0 de m*s0 thoa man PKCS 
print("[*] step 1 : searching for s1 ")
s1 = n // B3 

while True :
	s1 += 1 
	if PKCS1(s1):
		break 
setN = set([])
m1 = s1 * m0 
for r in range(ceil(B2*s1 - B3 + 1,n),floor(B3*s1 - B2,n) + 1):
	lbound = max(ceil(B2 + r*n,s1) , B2)
	ubound = min(floor(B3-1 + r*n,s1) , B3)
	if lbound <= ubound :
		setN |= set([(ceil(B2 + r*n,s1),floor(B3 + r * n,s1))]) 
#step 2 : searching for PKCS conforming  messages
si = s1  
i = 0 
while (True) : 
	i += 1
	print("[*] [*] [*] times : %d" % i) 
	print("[*] step 2 : searching for PKCS conforming messages")
	# searching with more than one interval left 
	if len(setN) > 1 :
		print("	[*] step 2.b: searching with more than one interval left") 
		while True : 
			si += 1
			if PKCS1(si) :
				break
	if len(setN) == 1 : 
		print("	[*] step 2.c: searching with exactly one interval left")
		loner = setN.pop()
		setN.add(loner)
		lower,upper = loner 
		ri = ceil(2*(upper*si - B2),n) 
		found = False 
		while not found : 
			for si in range(ceil(B2 + ri*n,upper),floor(B3 + ri*n,lower) + 1):
				if PKCS1(si):
					found  = True 	
					break 
				ri += 1 
	# step 3 : Narrow the set of solution 
	print("[*] step 3 : Narrow the interval")
	setN_temp = set([])
	for (a,b) in setN:
		for ri in range(ceil(a*si - B3 + 1,n),floor(b*si - B2,n) + 1):
			lbound = max(a,ceil(B2 + ri*n , si))
			ubound = min(b,floor(B3 - 1 + ri*n , si))
			print("the distinct = %d " % (ubound - lbound))
			if lbound <= ubound :
				setN_temp |= set([(lbound,ubound)])
				
	if len(setN_temp) > 0 : 
		setN = setN_temp
	if len(setN) == 1 : 
		(lower,upper) = setN.pop()
		setN.add((lower,upper))
		if lower == upper :
			print("[*] step 4: Computing the solution ")
			print("m = %d" %lower)
			break  


from random import randint 
from gmpy2 import invert
from hashlib import sha1 
from Crypto.Util.number import bytes_to_long

p = 0x800000000000000089e1855218a0e7dac38136ffafa72eda7859f2171e25e65eac698c1702578b07dc2a1076da241c76c62d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebeac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc871a584471bb1
q = 0xf4f47f05794b256174bba6e9b396a7707e563c5b

class DSA:
	def taoKhoa(self):
		z = (p-1) // q 
		h = randint(2,p-1)
		g = pow(h,z,p)
		self.x = randint(1,q-1)
		y = pow(g,self.x,p)
		return (g,y) 

	def Ky(self,message):
		while True:
			k = randint(1,q-1)
			r = pow(g,k,p) % q 
			s = invert(k,q)*(bytes_to_long(sha1(message).digest()) + r * self.x) % q
			if (r !=0 and s!=0):
				break
		return (r,s)

if __name__ == '__main__':
	DSA = DSA()
	message = b"Hi mom"
	g,y = DSA.taoKhoa()
	r,s = DSA.Ky(message)
	#confirm 
	if (0 < r and 0 < s and r < q and s < q):
		w = invert(s,q)
		u1 = w * bytes_to_long(sha1(message).digest())% q   
		u2 = r * w % q 
		v = pow(g,u1,p) * pow(y,u2,p) % p % q 
		if v==r : 
			print("OK")
		else :
			print("NO")
			print(v)
			print(r)


''' implement SRP ''' 
from gmpy2 import next_prime
from random import randint
from Crypto.Util.number import bytes_to_long
from os import urandom 
from hashlib import sha1

N = next_prime(randint(10**100,10**101))
g = 2 
k = 3 
password = urandom(16)

class server:
	def __init__(self):
		self.salt = urandom(16)
		self.b = randint(2,N)
	def recvACK(self,client):
		self.A = client.sendACK()
	def sendB(self):
		xH = sha1(self.salt + password).digest()
		x = bytes_to_long(xH)
		self.v = pow(g,x,N)
		B = k*self.v + pow(g,self.b,N)
		return B 
	def confirmEmail(self,client):
		S = pow(self.A,self.b,N)  
		if S == client.sendS():
			print ("OK")
		else :
			print ("KO")
			
class client:
	def __init__(self,password=password):
		self.a = 1 
		self.password = password
	def sendACK(self):
		self.a = randint(2,N) 
		return pow(g,self.a,N)
	def recvB(self,server):
		self.B = server.sendB()
	def computeS(self,server):
		xH = sha1(server.salt + self.password).digest()
		x = bytes_to_long(xH)
		v = pow(g,x,N)
		self.S = pow(self.B - k*v,self.a,N)
	def sendS(self):
		return self.S   

if __name__=='__main__':
	S = server()
	C = client(password)
	C.sendACK()
	S.recvACK(C)
	S.sendB()
	C.recvB(S)
	C.computeS(S)
	C.sendS()
	S.confirmEmail(C)

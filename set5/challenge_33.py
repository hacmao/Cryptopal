from random import randint 
p= 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2
class Alice : 
    def __init__(self): 
        self.a = randint(1,p-1) 

    def sendA(self):
        return pow(g,self.a,p) 

    def recvB(self,Bob):
        self.B =  Bob.sendB() 
        return self.B 

    def secret(self):
        return pow(self.B,self.a,p) 

class Bob: 
    def __init__ (self): 
        self.b = randint(1,p-1) 
    
    def sendB(self):
        return pow(g,self.b,p) 
    
    def recvA(self,Alice):
        self.A = Alice.sendA() 
        return self.A 
    
    def secret(self):
        return pow(self.A,self.b,p) 
    
if __name__ == '__main__':
    bob = Bob()
    alice = Alice() 
    A = bob.recvA(alice) 
    B = alice.recvB(bob) 
    if bob.secret() == alice.secret():
        print("Implemented Diffie hellman!")

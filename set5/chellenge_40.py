'''Implement an E=3 RSA Broadcast attack'''
from gmpy2 import iroot,invert,next_prime
from random import randint 

class Broadcast : 
    def __init__ (self,c1,c2,c3,N1,N2,N3): 
        self.c1 = c1 
        self.c2 = c2 
        self.c3 = c3 
        self.N1 = N1
        self.N2 = N2 
        self.N3 = N3  
    
    def solve(self): 
        C = 0 
        C += self.c1*self.N2*self.N3 * invert(self.N2*self.N3,self.N1) 
        C += self.c2*self.N1*self.N3 * invert(self.N1*self.N3,self.N2) 
        C += self.c3*self.N1*self.N2 * invert(self.N1*self.N2,self.N3) 
        C %= self.N1 * self.N2 * self.N3
        return iroot(C,3)[0]

if __name__ == "__main__":
    e = 3 
    a = 10**100
    b = 10**101 
    N1 = next_prime(randint(a,b)) * next_prime(randint(a,b))
    N2 = next_prime(randint(a,b)) * next_prime(randint(a,b))
    N3 = next_prime(randint(a,b)) * next_prime(randint(a,b)) 
    x = randint(2,min(N1,N2,N3)) 
    C1 = pow(x,3,N1) 
    C2 = pow(x,3,N2)
    C3 = pow(x,3,N3)
    broadcast = Broadcast(C1,C2,C3,N1,N2,N3) 
    assert x == broadcast.solve()


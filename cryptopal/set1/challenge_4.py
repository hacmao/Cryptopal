import challenge3
import string 

alphabeta = string.ascii_letters + " .?'\n" + string.digits
def isalphabeta(m):
    for ch in m : 
        if ch  not in  alphabeta : 
            return False 
    return True 

f = open("set1/4.txt","r")
M = f.readlines()
for i in range(len(M)):
    M[i] = M[i].strip("\n")

for i in range(len(M)):
    for j in range(256):
        p = challenge3.xor(M[i],chr(j)) 
        if isalphabeta(p):
            print("***********")
            print(i)
            print(p.encode('utf-8'))

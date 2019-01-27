''' challenge nay ko hay lam 
MT19937 nhan vao mot seed la ham theo thoi gian va minh break no bang cach doan seed thoi 
cach nay goi y cho ta mot lo hong la neu du doan duoc chuong trinh chay trong khoang thoi gian nao thi co the  
brute force de tim seed '''
import time 
from challenge_21 import MT19937 
from Crypto.Random import random

seed = int(time.time()) 
one = MT19937(seed)
x = one.uint32()

time.sleep(random.randint(4,10)) 

seed2 = int(time.time()) 
for i in range(10):
    seed_guess = seed2 - i 
    two = MT19937(seed_guess) 
    y = two.uint32()
    if y == x : 
        print("seed la : %d " % seed_guess)
        print("time sleep : %d " % i)

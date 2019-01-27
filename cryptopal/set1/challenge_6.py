''' Break vignere cipher 
Tinh chat : Hamming distance giua cac tu trong tieng anh thuong be hon trong cac tu ngau nhien 
Vi : trong tieng anh cac chu hau nhu la nam lower case letter co 99 <= ord <= 122 nen distance be 
Con trong cac ki tu ngau nhien thi hamming distance la cua cac ord trong khoang (1,128) do do distance lon 
Bai nay du doan length key , tim hamming distance trung binh cua ki tu doi voi tung lenkey (2,40)
Do : hamming distance giua hai cipher block  = hamming distance giua hai plaintext block tuong ung vi cung xor vs 1 key
Hamming distance nho nhat co kha nang cao la len key 
Chon lay 3 - 4 lenkey xong tien hanh tim key 
'''
from base64 import b64decode 
from math import ceil 
from string import ascii_letters,digits 
from challenge_4 import isalphabeta

alphabeta = ascii_letters + digits + " \n!'.:?,"

def Hamming_distance(a,b):
    H_distance = 0 
    for a0, b0 in zip (a,b):
        xor = bin(a0 ^ b0)[2:]
        for ch in xor : 
            if ch == "1" : 
                H_distance += 1 
    return H_distance 

def splitBlock(m,length):
    m_block = []
    for i in range(ceil(len(m)/length)) :
        m_block.append(m[length*i : length*(i+1)])
    return m_block

f = open("set1/6.txt","r")
c = f.read()
c = b64decode(c)
#print(c)
normalize_H = []
print("[*] breaking key length...........")
for length in range(2,41):
    H = 0 
    c_block = splitBlock(c,length)
    l = len(c_block)
    time = 0 
    for i in range(l-1): 
        for j in range(i+1,l): 
            H += Hamming_distance(c_block[i],c_block[j]) 
            time += 1 
    normalize_H.append(H/length/time) #distance hamming per letter
possible_length = []
print("[*] guess possible key length..........")
for i in range(3):
    Min = min(normalize_H)
    for i in range(len(normalize_H)):
        if normalize_H[i] == Min:
            possible_length.append(i+2)
            normalize_H[i] = 10000
print("Possible keylength = ",possible_length)
print("[*] Breaking key with each possible length")
for len_key in possible_length : 
    print("******************************")
    print("[*] Breaking with len = %d ......." % len_key)
    c_block_pos = []
    for i in range(len_key):
        c_block_pos_i = []
        for j in range(len(c)):
            if j % len_key == i:
                c_block_pos_i.append(c[j])
        c_block_pos.append(c_block_pos_i)
    key = []
    for i in range(len_key):
        key_i = []
        for k in alphabeta:
            xor_string = ""
            for ch in c_block_pos[i]:
                xor_string += chr(ch ^ ord(k))
            if isalphabeta(xor_string):
                key_i.append(k) 
        key.append(key_i)
    print(key)
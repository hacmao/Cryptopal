from math import ceil 

f = open("set1/8.txt","r")
c = f.readlines()
for i in range(len(c)):
    c[i] = c[i].strip("\n")

def splitBlock(m,length):
    m_block = []
    for i in range(ceil(len(m)/length)):
        m_block.append(m[length*i : length*(i+1)])
    return m_block

for ci in c :
    ci_block = splitBlock(ci,16)
    if len(ci_block) != len(set(ci_block)):
        print("ECB detect!!")
        print(ci)



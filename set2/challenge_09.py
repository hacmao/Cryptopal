''' implemented PKCS7 padding ''' 
def PKCS7(m,length):
    ch = length - len(m) % length 
    return m + bytes([ch]) * ch  

def unPad(c):
    return c[:-c[-1]] 

if __name__ == '__main__':
    print(PKCS7(b"kamithantha",16))
    a = PKCS7(b"kami",16)
    print(unPad(a))

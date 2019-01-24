''' implemented repeated key xor ''' 
from binascii import hexlify 
def repeatedXor(string,key):
    xor = b""
    for i in range(len(string)):
        xor += bytes([ord(string[i]) ^ ord(key[i % len(key)])]) 
    return xor 
if __name__ == '__main__':
    string = 'Burning \'em, if you ain\'t quick and nimble\
    I go crazy when I hear a cymbal'
    key = "ICE"
    print(hexlify(repeatedXor(string,key)))

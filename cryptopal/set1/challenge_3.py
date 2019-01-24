''' single byte xor cipher ''' 
import string 
cipher = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def xor(string,ch):
    string_bytes = bytes.fromhex(string)
    return "".join([chr(a0 ^ ord(ch)) for a0 in string_bytes]) 

if __name__ == "__main__":
    alphabeta = string.ascii_letters + string.digits 
    for ch in alphabeta : 
        print(xor(cipher,ch))  
        ''' find meaning word ''' 


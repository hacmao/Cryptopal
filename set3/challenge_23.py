from challenge_21 import MT19937 

def get_bit(y,k):
    return (y >> k) & 1

def guess_right_bit(y,i,k):
    if i > (31 - k) : 
        bit = get_bit(y,i) 
    else : 
        bit = get_bit(y,i) ^ guess_right_bit(y,i+k,k)
    return bit 

def invert_right_xor(y,k): 
    z = 0 
    for i in range(31,-1,-1): 
        z += 2**i * guess_right_bit(y,i,k)
    return z 

def guess_left_xor_bit(y,i,k,and_):
    if i < k : 
        bit = get_bit(y,i)
    else : 
        bit = get_bit(y,i) ^ (guess_left_xor_bit(y,i-k,k,and_) & get_bit(and_,i)) 
    return bit 

def invert_left_and_xor(y,k,and_):
    z = 0 
    for i in range(32):
        z += 2**i * guess_left_xor_bit(y,i,k,and_)
    return z 

def revese_uint32(y):
    y = invert_right_xor(y,18)
    y = invert_left_and_xor(y,15,0xefc60000) 
    y = invert_left_and_xor(y,7,0x9d2c5680) 
    y = invert_right_xor(y,11)
    return y 

def guess_next_random():
    global _MT_ 
    for i in range(624):
        y = (_MT_[i] & 0x80000000) + (_MT_[(i+1) % 624] & 0x7fffffff)
        _MT_[i] = _MT_[(i + 397) % 624] ^ (y >> 1)
        if y % 2 != 0:
            _MT_[i] ^= 0x9908b0df
    y = []
    index = 0 
    for i in range(624):
        yi = _MT_[index]
        yi ^= (yi >> 11)
        yi ^= ((yi << 7) & 0x9d2c5680)
        yi ^= ((yi << 15) & 0xefc60000)
        yi ^= (yi >> 18)
        index = (index + 1) % 624
        y.append(yi)
    return y

if __name__ == '__main__':
    seed = 12345
    r = MT19937(seed) 
    ''' generate 624 y value and 624 next value ''' 
    print("[*] Generate 624 value from MT19937........")
    y = []
    for i in range(624):
        y.append(r.uint32()) 
    y_next = []
    for i in range(624):
        y_next.append(r.uint32())
    ''' reverse _MT ''' 
    print("[*] Guess MT and 624 next value.........")
    _MT_ = [] 
    for yi in y : 
        _MT_.append(revese_uint32(yi))
    y_next_guess = guess_next_random()
    print("[*] Checking guess value.......")
    assert y_next_guess == y_next 
    print("True")
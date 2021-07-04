from random import randint

# function for extended Euclidean Algorithm  
def gcdExtended(a, b):  
    # Base Case  
    if a == 0 :   
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a)  
     
    # Update x and y using results of recursive  
    # call  
    x = y1 - (b//a) * x1  
    y = x1  
     
    return gcd,x,y 

def inverse(a, n):
    _, x, _ = gcdExtended(a%n, n)
    return x % n

class ECC:
    def __init__(self):
        self.p = 0xFFFFFFFE_FFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_00000000_FFFFFFFF_FFFFFFFF
        self.a = 0xFFFFFFFE_FFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF_00000000_FFFFFFFF_FFFFFFFC
        self.b = 0x28E9FA9E_9D9F5E34_4D5A9E4B_CF6509A7_F39789F5_15AB8F92_DDBCBD41_4D940E93
        self.n = 0xFFFFFFFE_FFFFFFFF_FFFFFFFF_FFFFFFFF_7203DF6B_21C6052B_53BBF409_39D54123
        self.Gx = 0x32C4AE2C_1F198119_5F990446_6A39C994_8FE30BBF_F2660BE1_715A4589_334C74C7
        self.Gy = 0xBC3736A2_F4F6779C_59BDCEE3_6B692153_D0A9877C_C62A4740_02DF32E5_2139F0A0
        self.d = randint(1, self.n - 1)
        self.Qx, self.Qy = self.multiply(self.d, self.Gx, self.Gy)
    
    def encrypt(self, m):
        while True:
            k = randint(1, self.n - 1)
            x1, y1 = self.multiply(k, self.Gx, self.Gy)
            x2, y2 = self.multiply(k, self.Qx, self.Qy)
            if x2 != 0:
                break
        C = m * x2 % self.n
        return x1, y1, C
    
    def decrypt(self, enc):
        x1, y1, C = enc
        x2, y2 = self.multiply(self.d, x1, y1)
        m = C * inverse(x2, self.n) % self.n
        return m

    def dup(self, x, y):
        la = ((3*x*x + self.a) * inverse(2*y, self.p)) % self.p
        x3 = (la*la - 2*x) % self.p
        y3 = (la * (x-x3) - y) % self.p
        return x3, y3
    
    def add(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return self.dup(x1, y1)
        elif x1 == x2 and (y1 + y2) % self.p == 0:
            return float("inf"), float("inf")
        elif x1 == float("inf") and y1 == float("inf"):
            return x2, y2
        elif x2 == float("inf") and y2 == float("inf"):
            return x1, y1
        la = ((y2-y1) * inverse(x2-x1, self.p)) % self.p
        x3 = (la*la - x1 - x2) % self.p
        y3 = (la * (x1-x3) - y1) % self.p
        return x3, y3
    
    def multiply(self, k, x, y):
        resultX = resultY = float("inf")
        while k > 0:
            if k & 1:
                resultX, resultY = self.add(resultX, resultY, x, y)
            k = k >> 1
            x, y = self.dup(x, y)
        return resultX, resultY

if __name__ == "__main__":
    msg = 0x123456789987654321abcdefedbca
    eccBlock = ECC()
    enc = eccBlock.encrypt(msg)
    rec = eccBlock.decrypt(enc)
    print("原文：0x%x" % msg)
    print("密文：X1: (0x%x, \n      0x%x)" % (enc[0], enc[1]))
    print("      C: 0x%x" % enc[2])
    print("解密：0x%x" % rec)
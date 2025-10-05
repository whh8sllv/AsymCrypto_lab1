import random

class Generator():

    def __init__(self, length):
        self.length = length
        self.m = 2**32
        self.a = 2**16 + 1
        self.c = 119     

    
    '''Built-in pseudo-random number generator: Python Random Module'''
    def python_random_generator(self):
        res = []
        for i in range(self.length):
            res.append(random.randint(0, 255))
        return bytes(res)
    
    
    '''LehmerLow Generator'''
    def lehmer_low_generator(self):
        x_0 = random.randint(1, self.m - 1)
        res = []
        for i in range(self.length):
            x_next = (self.a * x_0 + self.c) % self.m
            x_0 = x_next
            res.append(x_next)
        res_bytes = []
        for num in res:
            num_bin32 = format(num, '032b')
            res_bytes.append(int(num_bin32[-8:], 2))
        return bytes(res_bytes)


    '''LehmerHigh Generator'''
    def lehmer_high_generator(self):
        x_0 = random.randint(1, self.m - 1)
        res = [x_0]
        for i in range(self.length):
            x_next = (self.a * x_0 + self.c) % self.m
            x_0 = x_next
            res.append(x_next)
        res_bytes = []
        for num in res:
            num_bin32 = format(num, '032b')
            res_bytes.append(int(num_bin32[:8], 2))
        return bytes(res_bytes)
    

    '''L20 Generator'''
    def l20_generator(self):
        first_20 = []
        while True:
            for i in range(20):
                first_20.append(random.randint(0, 1))
            if sum(first_20) > 0:
                break
        res = first_20
        for t in range(20, self.length):
            x_t = res[t-3] ^ res[t-5] ^ res[t-9] ^ res[t-20]
            res.append(x_t)
        return ''.join([str(n) for n in res])
    
    '''L89 Generator'''
    def l89_generator(self):
        first_89 = []
        while True:
            for i in range(89):
                first_89.append(random.randint(0, 1))
            if sum(first_89) > 0:
                break
        res = first_89
        for t in range(89, self.length):
            x_t = res[t-38] ^ res[t-89]
            res.append(x_t)
        return ''.join([str(n) for n in res])



        
            

# python_random_module = Generator(10).python_random_generator()
# print(python_random_module)

# lehmer_low = Generator(10).lehmer_low_generator()
# print(lehmer_low)

# lehmer_high = Generator(10).lehmer_high_generator()
# print(lehmer_high)

# generator_l20 = Generator(2300).l20_generator()
# print(generator_l20)

generator_l89 = Generator(2300).l89_generator()
print(generator_l89)


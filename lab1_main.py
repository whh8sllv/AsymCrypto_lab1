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
    

    '''Geffe generator'''
    def geffe_generator(self):
        while True:
            l11 = [random.randint(0, 1) for i in range(11)]
            l9 = [random.randint(0, 1) for i in range(9)]
            l10 = [random.randint(0, 1) for i in range(10)]
            if sum(l11) > 0 and sum(l9) > 0 and sum(l10) > 0:
                break
        res_z = []
        for i in range(self.length):
            x_i = l11[len(l11)-11] ^ l11[len(l11)-9]
            y_i = l9[len(l9)-9] ^ l9[len(l9)-8] ^ l9[len(l9)-6] ^ l9[len(l9)-5]
            s_i = l10[len(l10)-10] ^ l10[len(l10)-7]

            z_i = (s_i & x_i) ^ ((1 ^ s_i) & y_i)
            res_z.append(z_i)

            l11.append(x_i)
            l9.append(y_i)
            l10.append(s_i)

        return ''.join([str(z) for z in res_z])
        
                    
# python_random_module = Generator(10).python_random_generator()
# print(python_random_module)

# lehmer_low = Generator(10).lehmer_low_generator()
# print(lehmer_low)

# lehmer_high = Generator(10).lehmer_high_generator()
# print(lehmer_high)

# generator_l20 = Generator(2300).l20_generator()
# print(generator_l20)

# generator_l89 = Generator(2300).l89_generator()
# print(generator_l89)

geffe_generator = Generator(1000000).geffe_generator()
print(geffe_generator)

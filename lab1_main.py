import random
from collections import Counter
from math import sqrt
from scipy.stats import norm

class Generator():

    def __init__(self, length=None):
        self.length = length
        self.m = 2**32
        self.a = 2**16 + 1
        self.c = 119
        self.BM_p = 0xcea42b987c44fa642d80ad9f51f10457690def10c83d0bc1bcee12fc3b6093e3
        self.BM_a = 0x5b88c41246790891c095e2878880342e88c79974303bd0400b090fe38a688356
        self.BBS_p = 0xd5bbb96d30086ec484eba3d7f9caeb07
        self.BBS_q = 0x425d2b9bfdb25b9cf6c416cc6e37b59c1f


    def left_shift(self, bits, n):
        return ((bits << n) | (bits >> (32 - n))) & (self.m - 1)
    

    def right_shift(self, bits, n):
        return ((bits >> n) | (bits << (32 - n))) & (self.m - 1)    
    

    def get_bits_into_bytes(self, bits):
        res = []
        if len(bits) % 8 != 0:
            r = len(bits) % 8
            dif = 8 - r
            bits += [0] * dif
        byte = ''
        for b in bits:
            byte += str(b)
            if len(byte) == 8:
                res.append(byte)
                byte = ''
        res_bin = [int(b, 2) for b in res]
        return bytes(res_bin)
        
    
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
        return self.get_bits_into_bytes(res)
    

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
        return self.get_bits_into_bytes(res)
    

    '''Geffe Generator'''
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

        return self.get_bits_into_bytes(res_z)
    
    '''Librarian Generator'''
    def librarian_generator(self, plaintext):
        with open(plaintext, 'rb') as text_bytes:
            bytes_string = text_bytes.read()
        return bytes_string
    

    '''Wolfram Generator'''
    def wolfram_generator(self):
        r_i = random.randint(1, self.m - 1)
        res = []
        for i in range(self.length):
            x_i = r_i % 2
            r_i = (self.left_shift(r_i, 1)) ^ (r_i | (self.right_shift(r_i, 1)))
            res.append(x_i)
        return self.get_bits_into_bytes(res)
    

    '''BM Generator'''
    def BM_generator(self):
        compare = int((self.BM_p - 1) / 2)
        t = random.randint(0, self.BM_p - 1)
        res = []
        for i in range(self.length):
            if t < compare:
                res.append(1)
            elif t >= compare:
                res.append(0)
            t = pow(self.BM_a, t, self.BM_p)
        return self.get_bits_into_bytes(res)
            

    '''BM bytes Generator'''
    def BM_bytes_generator(self):
        t = random.randint(0, self.BM_p - 1)
        res = []
        for i in range(self.length):
            k = int((256 * t) / (self.BM_p - 1))
            t = pow(self.BM_a, t, self.BM_p)
            res.append(k)
        return bytes(res)


    '''BBS Generator'''
    def BBS_generator(self):
        n = self.BBS_p * self.BBS_q
        r = random.randint(2, n-1)
        res = []
        for i in range(self.length):
            r = pow(r, 2, n)
            res.append(r % 2)
        return self.get_bits_into_bytes(res)


    '''BBS bytes Generator'''
    def BBS_bytes_generator(self):
        n = self.BBS_p * self.BBS_q
        r = random.randint(2, n-1)
        res = []
        for i in range(self.length):
            r = pow(r, 2, n)
            res.append(r % 256)
        return bytes(res)
    
class ProbabilityQualityTest():

    def __init__(self, alpha, generator_bytes):
        self.alpha = alpha
        self.test_data = generator_bytes
        self.n = len(self.test_data) / 256

    def calculate_chi_square(self):
        chi_square = 0
        v = Counter(self.test_data)
        for j in range(256):
            chi_square += (((v[j] - self.n)**2) / self.n)
        return chi_square
    
    def calculate_limit_chi_square(self):
        l = 255
        z = norm.ppf(1 - self.alpha)
        return ((sqrt(2*l) * z) + l)
    
    def compare_data(self):
        print(f'Гіпотеза H_0: всі байти послідовності рівноімовірні')
        chi_square = self.calculate_chi_square()
        limit_chi_square = self.calculate_limit_chi_square()
        print(f'Статистика хі-квадрат = {chi_square}')
        print(f'Граничне значення хі-квадрат = {limit_chi_square} (l=255, alpha = {self.alpha})')
        if chi_square <= limit_chi_square:
            print(f'значення хі-квадрат не перевищує граничне значення хі-квадрат при alpha = {self.alpha}, тому гіпотеза H_0 не суперечить експериментальним даним і приймається')
            print('==> всі байти послідовності рівноімовірні')
        else:
            print(f'значення хі-квадрат перевищує граничне значення хі-квадрат при alpha = {self.alpha}, тому гіпотеза H_0 відкидається')
        


# python_random_module = Generator(125000).python_random_generator()
# print(python_random_module)
# print()

# probability_random_module_test = ProbabilityQualityTest(0.01, python_random_module).compare_data()




# lehmer_low = Generator(125000).lehmer_low_generator()
# print(lehmer_low)

# probability_lehmer_low_module_test = ProbabilityQualityTest(0.01, lehmer_low).compare_data()

# lehmer_high = Generator(100).lehmer_high_generator()
# print(lehmer_high)

# generator_l20 = Generator(2300).l20_generator()
# print(generator_l20)

# generator_l89 = Generator(2300).l89_generator()
# print(generator_l89)

geffe_generator = Generator(125000).geffe_generator()
print(geffe_generator)
print(f'кількість байтів = {len(geffe_generator)}')

probability_geffe = ProbabilityQualityTest(0.01, geffe_generator).compare_data()


# librarion = Generator().librarian_generator('orwell.txt')
# print(librarion)

# wolfram_generator = Generator(10000).wolfram_generator()
# print(wolfram_generator)

# BM = Generator(100).BM_generator()
# print(BM)

# BM_bytes = Generator(100).BM_bytes_generator()
# print(BM_bytes)

# bbs_generator = Generator(1000).BBS_generator()
# print(bbs_generator)

# bbs_bytes_generator = Generator(100).BBS_bytes_generator()
# print(bbs_bytes_generator)
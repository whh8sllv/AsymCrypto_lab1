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
            print(f'Значення хі-квадрат не перевищує граничне значення хі-квадрат при alpha = {self.alpha}, тому гіпотеза H_0 не суперечить експериментальним даним і приймається')
            print('==> всі байти послідовності рівноімовірні')
        else:
            print(f'Значення хі-квадрат перевищує граничне значення хі-квадрат при alpha = {self.alpha}, тому гіпотеза H_0 відкидається')



class IndependenceQualityTest():

    def __init__(self, alpha, generator_bytes):
        self.alpha = alpha
        self.test_data = generator_bytes
        self.n = len(self.test_data) // 2

    def get_pairs(self):
        pairs = []
        for i in range(1, self.n):
            pairs.append((self.test_data[2*i - 1], self.test_data[2*i]))
        return pairs
    
    def calculate_chi_square(self):
        chi_square = 0
        pairs = self.get_pairs()
        v_ij = Counter(pairs)
        bytes_i = [el[0] for el in pairs]
        bytes_j = [el[1] for el in pairs]
        v_i = Counter(bytes_i)
        al_j = Counter(bytes_j)
        for i in range(256):
            for j in range(256):
                v_pair = v_ij[(i, j)]
                v = v_i[i]
                al = al_j[j]
                if v_pair == 0 or v == 0 or al == 0:
                    continue
                chi_square += (v_pair**2 / (v*al))
        chi_square *= self.n
        chi_square -= self.n
        return chi_square
    
    def calculate_limit_chi_square(self):
        l = 255**2
        z = norm.ppf(1 - self.alpha)
        return ((sqrt(2*l) * z) + l)
    
    def compare_data(self):
        print(f'Гіпотеза H_0: байти послідовності незалежні від попереднього значення')
        chi_square = self.calculate_chi_square()
        limit_chi_square = self.calculate_limit_chi_square()
        print(f'Статистика хі-квадрат = {chi_square}')
        print(f'Граничне значення хі-квадрат = {limit_chi_square} (l=255^2, alpha = {self.alpha})')
        if chi_square <= limit_chi_square:
            print(f'Значення хі-квадрат не перевищує граничне значення хі-квадрат при alpha = {self.alpha}, тому гіпотеза H_0 не суперечить експериментальним даним і приймається')
            print('==> байти послідовності незалежні від попереднього значення')
        else:
            print(f'Значення хі-квадрат перевищує граничне значення хі-квадрат при alpha = {self.alpha}, тому гіпотеза H_0 відкидається')


class UniformityQualityTest():

    def __init__(self, alpha, generator_bytes):
        self.alpha = alpha
        self.test_data = generator_bytes
        self.n = len(self.test_data)
        self.r = 200
        self.m_i = self.n // self.r

    def get_sequences(self):
        seq = []
        for i in range(0, len(self.test_data), self.m_i):
            fragment = self.test_data[i:i+self.m_i]
            seq.append(fragment)
        return seq
    
    def calculate_chi_square(self):
        sequences = self.get_sequences()
        chi_square = 0
        v = Counter(self.test_data)
        for i in range(256):
            for j in sequences:
                v_ij = Counter(j)[i]
                v_i = v[i]
                if v_ij == 0 or v_i == 0:
                    continue
                chi_square += (v_ij**2 / (v_i * self.m_i))
        chi_square *= self.n
        chi_square -= self.n
        return chi_square
        
    def calculate_limit_chi_square(self):
        l = 255 * (self.r - 1)
        z = norm.ppf(1 - self.alpha)
        return ((sqrt(2*l) * z) + l)
    
    def compare_data(self):
        print(f'Гіпотеза H_0: послідовності байтів обираються з одного і того ж самого розподілу, послідовність є однорідною')
        chi_square = self.calculate_chi_square()
        limit_chi_square = self.calculate_limit_chi_square()
        print(f'Статистика хі-квадрат = {chi_square}')
        print(f'Граничне значення хі-квадрат = {limit_chi_square} (l=255*(r-1), alpha = {self.alpha}, r = {self.r})')
        if chi_square <= limit_chi_square:
            print(f'Значення хі-квадрат не перевищує граничне значення хі-квадрат при alpha = {self.alpha}, тому гіпотеза H_0 не суперечить експериментальним даним і приймається')
            print('==> послідовність є однорідною, байти обираються з одного розподілу')
        else:
            print(f'Значення хі-квадрат перевищує граничне значення хі-квадрат при alpha = {self.alpha}, тому гіпотеза H_0 відкидається')


def display():
    print('Оберіть, який генератор Ви хочете перевірити: ')
    print('1 - вбудований генератор мови програмування Python')
    print('2 - генератор LehmerLow')
    print('3 - генератор LehmerHigh')
    print('4 - генератор L20')
    print('5 - генератор L89')
    print('6 - генератор Джиффі (Geffe)')
    print('7 - генератор "Бібліотекар"')
    print('8 - генератор Вольфрама')
    print('9 - генератор Блюма-Мікалі ВМ')
    print('10 - ВМ_bytes (байтова модифікація генератору Блюма-Мікалі)')
    print('11 - генератор BBS')
    print('12 - генератор BBS_bytes (байтова модифікація генератору BBS)')
    n = int(input('Номер вашого піддослідного = '))
    if n == 1:
        print('Отже, перевіримо вбудований генератор мови програмування Python')
        byte_length = int(input('Зазначте довжину послідовності для генерування в байтах: '))
        alpha_level = float(input('Оберіть значення параметру alpha для перевірки гіпотез (0.01 / 0.05 / 0.1): '))
        print('Ваша послідовність генерується...')
        python_random_module = Generator(byte_length).python_random_generator()
        print('...')
        print('Послідовність згенеровано. Перевіримо її якість')
        print('***')
        ProbabilityQualityTest(alpha_level, python_random_module).compare_data()
        print('***')
        IndependenceQualityTest(alpha_level, python_random_module).compare_data()
        print('***')
        UniformityQualityTest(alpha_level, python_random_module).compare_data()
    elif n == 2:
        print('Отже, перевіримо генератор LehmerLow')
        byte_length = int(input('Зазначте довжину послідовності для генерування в байтах: '))
        alpha_level = float(input('Оберіть значення параметру alpha для перевірки гіпотез (0.01 / 0.05 / 0.1): '))
        print('Ваша послідовність генерується...')
        lehmer_low = Generator(byte_length).lehmer_low_generator()
        print('...')
        print('Послідовність згенеровано. Перевіримо її якість')
        print('***')
        ProbabilityQualityTest(alpha_level, lehmer_low).compare_data()
        print('***')
        IndependenceQualityTest(alpha_level, lehmer_low).compare_data()
        print('***')
        UniformityQualityTest(alpha_level, lehmer_low).compare_data()
    elif n == 3:
        print('Отже, перевіримо генератор LehmerHigh')
        byte_length = int(input('Зазначте довжину послідовності для генерування в байтах: '))
        alpha_level = float(input('Оберіть значення параметру alpha для перевірки гіпотез (0.01 / 0.05 / 0.1): '))
        print('Ваша послідовність генерується...')
        lehmer_high = Generator(byte_length).lehmer_high_generator()
        print('...')
        print('Послідовність згенеровано. Перевіримо її якість')
        print('***')
        ProbabilityQualityTest(alpha_level, lehmer_high).compare_data()
        print('***')
        IndependenceQualityTest(alpha_level, lehmer_high).compare_data()
        print('***')
        UniformityQualityTest(alpha_level, lehmer_high).compare_data()
    elif n == 4:
        print('Отже, перевіримо генератор L20')
        byte_length = int(input('Зазначте довжину послідовності для генерування в бітах: '))
        alpha_level = float(input('Оберіть значення параметру alpha для перевірки гіпотез (0.01 / 0.05 / 0.1): '))
        print('Ваша послідовність генерується...')
        l20 = Generator(byte_length).l20_generator()
        print('...')
        print('Послідовність згенеровано. Перевіримо її якість')
        print('***')
        ProbabilityQualityTest(alpha_level, l20).compare_data()
        print('***')
        IndependenceQualityTest(alpha_level, l20).compare_data()
        print('***')
        UniformityQualityTest(alpha_level, l20).compare_data()
    elif n == 5:
        print('Отже, перевіримо генератор L89')
        byte_length = int(input('Зазначте довжину послідовності для генерування в бітах: '))
        alpha_level = float(input('Оберіть значення параметру alpha для перевірки гіпотез (0.01 / 0.05 / 0.1): '))
        print('Ваша послідовність генерується...')
        l89 = Generator(byte_length).l89_generator()
        print('...')
        print('Послідовність згенеровано. Перевіримо її якість')
        print('***')
        ProbabilityQualityTest(alpha_level, l89).compare_data()
        print('***')
        IndependenceQualityTest(alpha_level, l89).compare_data()
        print('***')
        UniformityQualityTest(alpha_level, l89).compare_data()
    elif n == 6:
        print('Отже, перевіримо генератор Джиффі (Geffe)')
        byte_length = int(input('Зазначте довжину послідовності для генерування в бітах: '))
        alpha_level = float(input('Оберіть значення параметру alpha для перевірки гіпотез (0.01 / 0.05 / 0.1): '))
        print('Ваша послідовність генерується...')
        geffe = Generator(byte_length).geffe_generator()
        print('...')
        print('Послідовність згенеровано. Перевіримо її якість')
        print('***')
        ProbabilityQualityTest(alpha_level, geffe).compare_data()
        print('***')
        IndependenceQualityTest(alpha_level, geffe).compare_data()
        print('***')
        UniformityQualityTest(alpha_level, geffe).compare_data()
    elif n == 7:
        print('Отже, перевіримо генератор "Бібліотекар"')
        filename = input("Зазначте назву вхідного файлу, з якого буде генеруватись послідовність байтів (формат 'назва.txt'): ")
        alpha_level = float(input('Оберіть значення параметру alpha для перевірки гіпотез (0.01 / 0.05 / 0.1): '))
        print('Ваша послідовність генерується...')
        print('...')
        librarion = Generator().librarian_generator(filename)
        print(f'Послідовність згенеровано. Довжина послідовності дорівнює {len(librarion)} байтів')
        print('Перевіримо її якість')
        print('***')
        ProbabilityQualityTest(alpha_level, librarion).compare_data()
        print('***')
        IndependenceQualityTest(alpha_level, librarion).compare_data()
        print('***')
        UniformityQualityTest(alpha_level, librarion).compare_data()
    elif n == 8:
        print('Отже, перевіримо генератор Вольфрама')
        byte_length = int(input('Зазначте довжину послідовності для генерування в бітах: '))
        alpha_level = float(input('Оберіть значення параметру alpha для перевірки гіпотез (0.01 / 0.05 / 0.1): '))
        print('Ваша послідовність генерується...')
        wolfram = Generator(byte_length).wolfram_generator()
        print('...')
        print('Послідовність згенеровано. Перевіримо її якість')
        print('***')
        ProbabilityQualityTest(alpha_level, wolfram).compare_data()
        print('***')
        IndependenceQualityTest(alpha_level, wolfram).compare_data()
        print('***')
        UniformityQualityTest(alpha_level, wolfram).compare_data()
    elif n == 9:
        print('Отже, перевіримо генератор Блюма-Мікалі BM')
        byte_length = int(input('Зазначте довжину послідовності для генерування в бітах: '))
        alpha_level = float(input('Оберіть значення параметру alpha для перевірки гіпотез (0.01 / 0.05 / 0.1): '))
        print('Ваша послідовність генерується...')
        BM = Generator(byte_length).BM_generator()
        print('...')
        print('Послідовність згенеровано. Перевіримо її якість')
        print('***')
        ProbabilityQualityTest(alpha_level, BM).compare_data()
        print('***')
        IndependenceQualityTest(alpha_level, BM).compare_data()
        print('***')
        UniformityQualityTest(alpha_level, BM).compare_data()
    elif n == 10:
        print('Отже, перевіримо генератор BM_bytes (байтова модифікація генератору Блюма-Мікалі)')
        byte_length = int(input('Зазначте довжину послідовності для генерування в байтах: '))
        alpha_level = float(input('Оберіть значення параметру alpha для перевірки гіпотез (0.01 / 0.05 / 0.1): '))
        print('Ваша послідовність генерується...')
        BM_bytes = Generator(byte_length).BM_bytes_generator()
        print('...')
        print('Послідовність згенеровано. Перевіримо її якість')
        print('***')
        ProbabilityQualityTest(alpha_level, BM_bytes).compare_data()
        print('***')
        IndependenceQualityTest(alpha_level, BM_bytes).compare_data()
        print('***')
        UniformityQualityTest(alpha_level, BM_bytes).compare_data()
    elif n == 11:
        print('Отже, перевіримо генератор BBS')
        byte_length = int(input('Зазначте довжину послідовності для генерування в бітах: '))
        alpha_level = float(input('Оберіть значення параметру alpha для перевірки гіпотез (0.01 / 0.05 / 0.1): '))
        print('Ваша послідовність генерується...')
        BBS = Generator(byte_length).BBS_generator()
        print('...')
        print('Послідовність згенеровано. Перевіримо її якість')
        print('***')
        ProbabilityQualityTest(alpha_level, BBS).compare_data()
        print('***')
        IndependenceQualityTest(alpha_level, BBS).compare_data()
        print('***')
        UniformityQualityTest(alpha_level, BBS).compare_data()
    elif n == 12:
        print('Отже, перевіримо генератор BBS_bytes (байтова модифікація генератору BBS)')
        byte_length = int(input('Зазначте довжину послідовності для генерування в байтах: '))
        alpha_level = float(input('Оберіть значення параметру alpha для перевірки гіпотез (0.01 / 0.05 / 0.1): '))
        print('Ваша послідовність генерується...')
        BBS_bytes = Generator(byte_length).BBS_bytes_generator()
        print('...')
        print('Послідовність згенеровано. Перевіримо її якість')
        print('***')
        ProbabilityQualityTest(alpha_level, BBS_bytes).compare_data()
        print('***')
        IndependenceQualityTest(alpha_level, BBS_bytes).compare_data()
        print('***')
        UniformityQualityTest(alpha_level, BBS_bytes).compare_data()
    

display()
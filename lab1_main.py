import random

class Generator():

    def __init__(self, length):
        self.length = length
    
    '''Built-in pseudo-random number generator: Python Random Module'''
    def python_random(self):
        res = []
        for i in range(self.length):
            res.append(random.randint(0, 255))
        return bytes(res)
    


python_random_module = Generator(160).python_random()
print(python_random_module)

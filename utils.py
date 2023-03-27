import numpy as np
import random

trader_type = ['GVWY', 'ZIC', 'SHVR', 'SNPR', 'ZIP']

def offset_t(t):
    return int(0.1 * np.random.normal(t,5))

def offset_0(t):
    return int(np.random.normal(0,20))

envs = [offset_t,offset_0]

class mutate_strat_default: #m1
    def __init__(self):
        self.sdev = 0.05

    def __call__(self,s):
        newstrat = s
        while newstrat == s:
            newstrat = s + random.gauss(0.0, self.sdev)
            newstrat = max(-1.0, min(1.0, newstrat))
        return newstrat

class mutate_strat_default_largev(mutate_strat_default):    #m2
    def __init__(self):
        self.sdev = 0.15

class mutate_strat_sym: #m3
    def __init__(self):
        self.sign = 1

    def __call__(self,s):
        newstrat = s
        if (s == 1) and (self.sign == 1):
            return s
        if (s == -1) and (self.sign == -1):
            return s
        while newstrat == s:
            newstrat = s + self.sign * random.uniform(0.0, 0.1)
            newstrat = max(-1.0, min(1.0, newstrat))
        self.sign = -self.sign
        return newstrat

# class mutate_strat_bi:  #m4
#     def __init__(self):
#         self.sign = 1
#         self.sdev = 0.05

#     def __call__(self,s):
#         if s >= 0:
#             mean_d = (1 - s)/2
#         else:
#             mean_d = - (s + 1)/2
#         newstrat = s
#         while newstrat == s:
#             newstrat = random.gauss(s + self.sign * mean_d, self.sdev)
#             newstrat = max(-1.0, min(1.0, newstrat))
#         self.sign = -self.sign
#         return newstrat

#mutations = [mutate_strat_default,mutate_strat_default_largev,mutate_strat_sym,mutate_strat_bi]
mutations = [mutate_strat_default,mutate_strat_default_largev,mutate_strat_sym]

PRSH_paras = [[(0, 2, 256), (1, 2, 256), (2, 2, 256), (0, 4, 64), (0, 4, 128), (1, 4, 256), (2, 4, 256), (0, 6, 32), (2, 6, 128), (0, 10, 32), (2, 10, 256), (0, 12, 256), (1, 12, 128), (1, 12, 256), (2, 12, 256), (0, 14, 256), (1, 14, 64), (2, 14, 64), (2, 14, 128), (0, 16, 64), (0, 16, 256), (2, 16, 32), (2, 16, 256)],
[(0, 2, 64), (0, 2, 256), (1, 2, 64), (1, 2, 256), (2, 2, 32), (2, 2, 256), (0, 4, 32), (0, 4, 128), (0, 4, 256), (1, 4, 256), (2, 4, 128), (0, 6, 32), (1, 6, 128), (1, 6, 256), (2, 6, 32), (2, 6, 64), (2, 6, 128), (2, 6, 256), (0, 8, 32), (0, 8, 64), (2, 8, 64), (0, 10, 32), (0, 10, 64), (0, 10, 256), (1, 10, 32), (1, 10, 128), (2, 10, 128), (2, 10, 256), (0, 12, 64), (0, 12, 256), (1, 14, 32), (1, 14, 128), (1, 14, 256), (2, 14, 128), (2, 14, 256), (0, 16, 256), (1, 16, 256)]]

PRSH_bayesian_paras = [[(2, 32), (2, 64), (2, 256), (3, 32), (3, 64), (3, 128), (3, 256), (4, 32), (4, 64), (4, 256)],
[(2, 32), (2, 64), (2, 128), (2, 256), (3, 32), (3, 64), (3, 128), (3, 256), (4, 32), (4, 64), (4, 128), (4, 256)]]
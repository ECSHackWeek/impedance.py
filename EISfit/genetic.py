from .fitting import circuit_fit, computeCircuit
from .circuits import FlexiCircuit
from .circuit_elements import *
#import circuit_elements

import numpy as np


#print(l1)

def generate_circuit(length, parent=None):
    i=0
    elem = np.random.randint(0,length,size=length)
    l1 = ['R','C','W','A','E','G']
    out = "s("
    if parent is None:
        while i < length:
            par = np.random.random()

            if par < 0.2 and i < length-1:
                out += "p("
                out += l1[elem[i]]
                out += ','
                i += 1
                out += l1[elem[i]]
                out += ')-'
                i += 1
            else:
                out += l1[elem[i]]
                out += "-"
                i += 1
        out = out[:-1]
        out += ")"
        return out
    else:
        discrete_parts = parent.split('-')
        chance = np.random.rand(len(discrete_parts))
        for i in range(len(discrete_parts)):
            if chance[i] < 0.3:
                if i > 0:
                    out = ""
                else:
                    out = "s("
                par = np.random.random()
                if par < 0.2:
                    out += "p("
                    out += l1[elem[i]]
                    out += ','
#                    i += 1
                    out += l1[elem[i]]
                    out += ')'
#                    i += 1
                else:
                    out += l1[elem[i]]
#                    out += "-"
                if i == len(discrete_parts)-1:
                    out += ")"
                discrete_parts[i] = out
        to_out = []
        for i in discrete_parts:
            to_out.append(i)
            to_out.append('-')
        return ''.join(to_out[:-1])
                


def make_population(num, n, parent=None):
    gen = []
    if parent is None:
        for i in range(num):
            gen.append(generate_circuit(n,parent=parent))
    return gen

    


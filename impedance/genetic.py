import numpy as np


def generate_circuit(length, parent=None, mutate=0.3, parallel=0.2):
    i = 0
    elem = np.random.randint(0, length, size=length)
    l1 = ['R', 'C', 'W1/W2', 'A', 'E1/E2', 'G1/G2']
    out = ""
    if parent is None:
        while i < length:
            par = np.random.random()

            if par < parallel and i < length-1:
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
        out += ""
        return out
    else:
        discrete_parts = parent.split('-')
        chance = np.random.rand(len(discrete_parts))
        for i in range(len(discrete_parts)):
            if chance[i] < mutate:
                if i > 0:
                    out = ""
                else:
                    out = ""
                par = np.random.random()
                if par < parallel:
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
                    out += ""
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
            gen.append(generate_circuit(n, parent=parent))
    return gen

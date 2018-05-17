import EISfit
from EISfit.circuit_elements import *
import numpy as np

def correct_vals():
    funcs = [R,C,W,A,E,G]
    freqs = [0.0031623, 0.0039811, 0.0050119]
    correct_vals = [[0.1,0.1,0.1],[]]
    input_vals = [0.1,0.2]
    inputs = [1,1,2,1,2,2]
    count = 0
    val_list = []
    for f in funcs:
        val = f(input_vals[:inputs[count]],freqs)
        val_list.append(list(val))
        count+=1
    print(val_list)
    return val_list

def test_all():
    
    funcs = [R,C,W,A,E,G] # s,p
    freqs = [0.0031623, 0.0039811, 0.0050119]
    correct_vals = [[0.1, 0.1, 0.1],
             [-503.2885655753576j, -399.7763007507859j, -317.55410740815927j],
             [(0.03333332999119107-25.16443710957406j),
              (0.03333332803640355-19.988826154865095j),
              (0.03333332493829798-15.877719366267762j)],
             [(0.014095856446805211-0.014095856446805211j),
              (0.01581581140075104-0.01581581140075104j),
              (0.017745618174933597-0.017745618174933597j)],
             [(20.824267708927916-6.7662147382575775j),
              (19.887021101226527-6.461684855187921j),
              (18.991963740046767-6.170863089282367j)],
             [(0.2227851024868618-0.011039297623348644j),
              (0.22230990531584205-0.013848198887593144j),
              (0.22156478618085362-0.01733628284175942j)]]
    input_vals = [0.1,0.2]
    inputs = [1,1,2,1,2,2]
    count = 0
    for f in funcs:
        val = f(input_vals[:inputs[count]],freqs)
        for j in range(len(correct_vals[count])):
            assert cmath.isclose(val[j],correct_vals[count][j])
        
        # check for typing:
        try:
            f(1,2)
        except(AssertionError):
            pass
        else:
            raise Exception('unhandled error occurred')
        # test for handling more wrong inputs
        try:
            f(['hi'],['yes','hello'])
        except(AssertionError):
            pass
        else:
            raise Exception('unhandled error occurred')
        return
        count+=1
    pass

def test_s():
    
    pass

def test_p():
    pass


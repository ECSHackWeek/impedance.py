import EISfit
from EISfit.circuit_elements import *
import numpy as np

def correct_vals():
    funcs = [R,C,W,A,E,G]
    freqs = [0.0031623, 1.0, 1000]
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
    freqs = [0.0031623, 1.0, 1000]
    correct_vals = [[0.1, 0.1, 0.1],
         [-503.2885655753576j, -1.5915494309189535j, -0.0015915494309189533j],
         [(0.03333332999119107-25.16443710957406j),
          (0.03300437046673636-0.08232866785870396j),
          (0.0019947114020071634-0.0019947114020071634j)],
         [(0.014095856446805211-0.014095856446805211j),
          (0.25066282746310004-0.25066282746310004j),
          (7.926654595212021-7.926654595212021j)],
         [(20.824267708927916-6.7662147382575775j),
          (6.585220960717245-2.1396679941828154j),
          (1.6541327179718126-0.537460300252313j)],
         [(0.2227851024868618-0.011039297623348644j),
          (0.028647452492431665-0.02775008505285708j),
          (0.0008920762553460424-0.0008920478601288429j)]]
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


import EISfit
from EISfit.circuit_elements import *
import numpy as np

def test_s():
    
    pass

def test_p():
    pass

def test_R():
    # test for proper function
    val = R([0.1],[0.0031623, 0.0039811, 0.0050119])
    np.testing.assert_almost_equal(val, [0.1,0.1,0.1])
#    assert val.all() == [0.1, 0.1, 0.1].all()
#    val = EISfit.circuit_elements.R()
    # test for handling erronious inputs
    try:
        R(1,2)
    except(AssertionError):
        pass
    else:
        raise Exception('unhandled error occurred')
    # test for handling more wrong inputs
    try:
        R(['hi'],['yes','hello'])
    except(AssertionError):
        pass
    else:
        raise Exception('unhandled error occurred')
    return

def test_C():
    import cmath
    val = C([0.1],[0.0031623, 0.0039811, 0.0050119])
    assert cmath.isclose(val[0],-503.2885655753576j)
#    assert val.all() == [0.1, 0.1, 0.1].all()
#    val = EISfit.circuit_elements.R()
    # test for handling erronious inputs
    try:
        C(1,2)
    except(AssertionError):
        pass
    else:
        raise Exception('unhandled error occurred')
    # test for handling more wrong inputs
    try:
        C(['hi'],['yes','hello'])
    except(AssertionError):
        pass
    else:
        raise Exception('unhandled error occurred')
    return

def test_W():
    pass
    val = W([0.1,0.2],[0.0031623, 0.0039811, 0.0050119])
#    print(val)
    assert cmath.isclose(val[0],(0.03333332999119107-25.16443710957406j))
    # test for handling erronious inputs
    try:
        W(1,2)
    except(AssertionError):
        pass
    else:
        raise Exception('unhandled error occurred')
    # test for handling more wrong inputs
    try:
        W(['hi'],['yes','hello'])
    except(AssertionError):
        pass
    else:
        raise Exception('unhandled error occurred')
    return

def test_A():
    pass

def test_E():
    pass

def test_G():
    pass

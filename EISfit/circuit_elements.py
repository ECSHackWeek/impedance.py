import numpy as np
import cmath

def s(series):
    """ sums elements in series

    Notes
    ---------
    .. math::
        Z = Z_1 + Z_2 + ... + Z_n

    """
    z = len(series[0])*[0 + 0*1j]
    for elem in series:
        z += elem
    return z


def p(parallel):
    """ adds elements in parallel

    Notes
    ---------
    .. math::

        Z = \\frac{1}{\\frac{1}{Z_1} + \\frac{1}{Z_2} + ... + \\frac{1}{Z_n}}

     """
    z = len(parallel[0])*[0 + 0*1j]
    for elem in parallel:
        z += 1/elem
    return 1/z


def R(p, f):
    """ defines a resistor

    Notes
    ---------
    .. math::

        Z = R

    """
    assert type(p) == type([1.5]), 'Input must be of type list'
    assert type(p[0]) == type(2.5), 'list elements must be ints or floats'
    assert len(p) == 1, 'input list must be length 1'
    
    return np.array(len(f)*[p[0]])


def C(p, f):
    """ defines a capacitor

    .. math::

        Z = \\frac{1}{C \\times j 2 \\pi f}

     """
#    print(p)
    assert type(p) == type([1.5]), 'Input must be of type list'
    assert type(p[0]) == type(2.5), 'list elements must be ints or floats'
    assert len(p) == 1, 'input list must be length 1'
    
    omega = 2*np.pi*np.array(f)
    C = p[0]

    return 1.0/(C*1j*omega)


def W(p, f):
    """ defines a blocked boundary Finite-length Warburg Element

    Notes
    ---------
    .. math::
        Z = \\frac{R}{\\sqrt{ T \\times j 2 \\pi f}} \\coth{\\sqrt{T \\times j 2 \\pi f }}

    where :math:`R` = p[0] (Ohms) and :math:`T` = p[1] (sec) = :math:`\\frac{L^2}{D}`

    """
    assert type(p) == type([1.5]), 'Input must be of type list'
    assert type(p[0]) == type(2.5), 'list elements must be ints or floats'
    assert len(p) == 2, 'input list must be length 2'
    
    omega = 2*np.pi*np.array(f)

    Zw = np.vectorize(lambda y: p[0]/(np.sqrt(p[1]*1j*y)*cmath.tanh(np.sqrt(p[1]*1j*y))))

    return Zw(omega)


def A(p, f):
    """ defines a semi-infinite Warburg element

    """

    omega = 2*np.pi*np.array(f)
    Aw = p[0]

    Zw = Aw*(1-1j)*np.sqrt(omega)

    return Zw


def E(p, f):
    """ defines a constant phase element

    Notes
    -----
    .. math::

        Z = \\frac{1}{Q \\times (j 2 \\pi f)^\\alpha}

    where :math:`Q` = p[0] and :math:`\\alpha` = p[1].
    """

    omega = 2*np.pi*np.array(f)
    Q = p[0]
    alpha = p[1]

    return 1.0/(Q*(1j*omega)**alpha)


def G(p, f):
    """ defines a Gerischer Element

    Notes
    ---------
    .. math::

        Z = \\frac{1}{Y \\times \\sqrt{K + j 2 \\pi f }}

     """

    omega = 2*np.pi*np.array(f)
    Z0 = p[0]
    k = p[1]

    return Z0/np.sqrt(k + 1j*omega)

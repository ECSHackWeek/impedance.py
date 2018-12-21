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
    typeChecker(p, f, R.__name__, 1)
    return np.array(len(f)*[p[0]])


def C(p, f):
    """ defines a capacitor

    .. math::

        Z = \\frac{1}{C \\times j 2 \\pi f}

     """

    typeChecker(p, f, C.__name__, 1)
    omega = 2*np.pi*np.array(f)
    capacitance = p[0]

    return 1.0/(capacitance*1j*omega)


def L(p, f):
    """ defines an inductor

    .. math::

        Z = L \\times j 2 \\pi f

     """

    typeChecker(p, f, L.__name__, 1)
    omega = 2*np.pi*np.array(f)
    inductance = p[0]

    return inductance*1j*omega


def W(p, f):
    """ defines a blocked boundary Finite-length Warburg Element

    Notes
    ---------
    .. math::
        Z = \\frac{R}{\\sqrt{ T \\times j 2 \\pi f}} \\coth{\\sqrt{T \\times j 2 \\pi f }}  # noqa: E501

    where :math:`R` = p[0] (Ohms) and
    :math:`T` = p[1] (sec) = :math:`\\frac{L^2}{D}`

    """

    typeChecker(p, f, W.__name__, 2)

    omega = 2*np.pi*np.array(f)

    Zw = np.vectorize(lambda y: p[0]/(np.sqrt(p[1]*1j*y) *
                                      cmath.tanh(np.sqrt(p[1]*1j*y))))

    return Zw(omega)


def A(p, f):
    """ defines a semi-infinite Warburg element

    """

    typeChecker(p, f, A.__name__, 1)
    omega = 2*np.pi*np.array(f)
    Aw = p[0]

    Zw = Aw*(1-1j)/np.sqrt(omega)

    return Zw


def E(p, f):
    """ defines a constant phase element

    Notes
    -----
    .. math::

        Z = \\frac{1}{Q \\times (j 2 \\pi f)^\\alpha}

    where :math:`Q` = p[0] and :math:`\\alpha` = p[1].
    """
    typeChecker(p, f, E.__name__, 2)
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
    typeChecker(p, f, G.__name__, 2)
    omega = 2*np.pi*np.array(f)
    Z0 = p[0]
    k = p[1]

    return Z0/np.sqrt(k + 1j*omega)


def K(p, f):
    """ An RC element for use in lin-KK model

    Notes
    -----
    .. math::

        Z = \\frac{R}{1 + j \\omega \\tau_k}

    """

    omega = np.array(f)

    return p[0]/(1 + 1j*omega*p[1])


def typeChecker(p, f, name, length):
    assert isinstance(p, list), \
        'in {}, input must be of type list'.format(name)
    for i in p:
        assert isinstance(i, (float, int, np.int32, np.float64)), \
            'in {}, value {} in {} is not a number'.format(name, i, p)
    for i in f:
        assert isinstance(i, (float, int, np.int32, np.float64)), \
            'in {}, value {} in {} is not a number'.format(name, i, f)
    assert len(p) == length, \
        'in {}, input list must be length {}'.format(name, length)
    return

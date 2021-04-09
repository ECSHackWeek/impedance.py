import numpy as np

initial_state = globals().copy()
non_element_functions = ['element_metadata',
                         'initial_state',
                         'non_element_functions',
                         'typeChecker',
                         'circuit_elements']
# populated at the end of the file -
# this maps ex. 'R' to the function R to always give us a list of
# active elements in any context
circuit_elements = {}


def element_metadata(num_params, units):
    """ decorator to store metadata for a circuit element

        Parameters
        ----------
        num_params : int
            number of parameters for an element
        units : list of str
            list of units for the element parameters
    """
    def decorator(func):
        def wrapper(p, f):
            typeChecker(p, f, func.__name__, num_params)
            return func(p, f)

        wrapper.num_params = num_params
        wrapper.units = units
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__

        return wrapper
    return decorator


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


@element_metadata(num_params=1, units=['Ohm'])
def R(p, f):
    """ defines a resistor

    Notes
    ---------
    .. math::

        Z = R

    """
    R = p[0]
    Z = np.array(len(f)*[R])
    return Z


@element_metadata(num_params=1, units=['F'])
def C(p, f):
    """ defines a capacitor

    .. math::

        Z = \\frac{1}{C \\times j 2 \\pi f}

     """
    omega = 2*np.pi*np.array(f)
    C = p[0]
    Z = 1.0/(C*1j*omega)
    return Z


@element_metadata(num_params=1, units=['H'])
def L(p, f):
    """ defines an inductor

    .. math::

        Z = L \\times j 2 \\pi f

     """
    omega = 2*np.pi*np.array(f)
    L = p[0]
    Z = L*1j*omega
    return Z


@element_metadata(num_params=1, units=['Ohm sec^-1/2'])
def W(p, f):
    """ defines a semi-infinite Warburg element

    Notes
    -----
    .. math::

        Z = \\frac{A_W}{\\sqrt{ 2 \\pi f}} (1-j)
    """
    omega = 2*np.pi*np.array(f)
    Aw = p[0]
    Z = Aw*(1-1j)/np.sqrt(omega)
    return Z


@element_metadata(num_params=2, units=['Ohm', 'sec'])
def Wo(p, f):
    """ defines an open (finite-space) Warburg element

    Notes
    ---------
    .. math::
        Z = \\frac{Z_0}{\\sqrt{ j \\omega \\tau }}
        \\coth{\\sqrt{j \\omega \\tau }}

    where :math:`Z_0` = p[0] (Ohms) and
    :math:`\\tau` = p[1] (sec) = :math:`\\frac{L^2}{D}`

    """
    omega = 2*np.pi*np.array(f)
    Z0, tau = p[0], p[1]
    Z = Z0/(np.sqrt(1j*omega*tau)*np.tanh(np.sqrt(1j*omega*tau)))
    return Z  # Zw(omega)


@element_metadata(num_params=2, units=['Ohm', 'sec'])
def Ws(p, f):
    """ defines a short (finite-length) Warburg element

    Notes
    ---------
    .. math::
        Z = \\frac{Z_0}{\\sqrt{ j \\omega \\tau }}
        \\tanh{\\sqrt{j \\omega \\tau }}

    where :math:`Z_0` = p[0] (Ohms) and
    :math:`\\tau` = p[1] (sec) = :math:`\\frac{L^2}{D}`

    """
    omega = 2*np.pi*np.array(f)
    Z0, tau = p[0], p[1]
    Z = Z0*np.tanh(np.sqrt(1j*omega*tau))/np.sqrt(1j*omega*tau)
    return Z


@element_metadata(num_params=2, units=['Ohm^-1 sec^a', ''])
def CPE(p, f):
    """ defines a constant phase element

    Notes
    -----
    .. math::

        Z = \\frac{1}{Q \\times (j 2 \\pi f)^\\alpha}

    where :math:`Q` = p[0] and :math:`\\alpha` = p[1].
    """
    omega = 2*np.pi*np.array(f)
    Q, alpha = p[0], p[1]
    Z = 1.0/(Q*(1j*omega)**alpha)
    return Z


@element_metadata(num_params=2, units=['H sec', ''])
def La(p, f):
    """ defines a modified inductance element as represented in [1]

    Notes
    -----
    .. math::

        Z = L \\times (j 2 \\pi f)^\\alpha

    where :math:`L` = p[0] and :math:`\\alpha` = p[1]

    [1] `EC-Lab Application Note 42, BioLogic Instruments (2019)
    <https://www.biologic.net/documents/battery-eis-modified-inductance-element-electrochemsitry-application-note-42>`_.
    """
    omega = 2*np.pi*np.array(f)
    L, alpha = p[0], p[1]
    Z = (L*1j*omega)**alpha
    return Z


@element_metadata(num_params=2, units=['Ohm', 'sec'])
def G(p, f):
    """ defines a Gerischer Element as represented in [1]

    Notes
    ---------
    .. math::

        Z = \\frac{R_G}{\\sqrt{1 + j \\, 2 \\pi f \\, t_G}}

    where :math:`R_G` = p[0] and :math:`t_G` = p[1]

    Gerischer impedance is also commonly represented as [2]:

    .. math::

        Z = \\frac{Z_o}{\\sqrt{K+ j \\, 2 \\pi f}}

    where :math:`Z_o = \\frac{R_G}{\\sqrt{t_G}}`
    and :math:`K = \\frac{1}{t_G}`
    with units :math:`\\Omega sec^{1/2}` and
    :math:`sec^{-1}` , respectively.

    [1] Y. Lu, C. Kreller, and S.B. Adler,
    Journal of The Electrochemical Society, 156, B513-B525 (2009)
    `doi:10.1149/1.3079337
    <https://doi.org/10.1149/1.3079337>`_.

    [2] M. González-Cuenca, W. Zipprich, B.A. Boukamp,
    G. Pudmich, and F. Tietz, Fuel Cells, 1,
    256-264 (2001) `doi:10.1016/0013-4686(93)85083-B
    <https://doi.org/10.1016/0013-4686(93)85083-B>`_.
     """
    omega = 2*np.pi*np.array(f)
    R_G, t_G = p[0], p[1]
    Z = R_G/np.sqrt(1 + 1j*omega*t_G)
    return Z


@element_metadata(num_params=3, units=['Ohm', 'sec', ''])
def Gs(p, f):
    """ defines a finite-length Gerischer Element as represented in [1]

    Notes
    ---------
    .. math::

        Z = \\frac{R_G}{\\sqrt{1 + j \\, 2 \\pi f \\, t_G} \\,
        tanh(\\phi \\sqrt{1 + j \\, 2 \\pi f \\, t_G})}

    where :math:`R_G` = p[0], :math:`t_G` = p[1] and :math:`\\phi` = p[2]

    [1] R.D. Green, C.C Liu, and S.B. Adler,
    Solid State Ionics, 179, 647-660 (2008)
    `doi:10.1016/j.ssi.2008.04.024
    <https://doi.org/10.1016/j.ssi.2008.04.024>`_.
     """
    omega = 2*np.pi*np.array(f)
    R_G, t_G, phi = p[0], p[1], p[2]
    Z = R_G/(np.sqrt(1 + 1j*omega*t_G) *
             np.tanh(phi * np.sqrt(1 + 1j*omega*t_G)))
    return Z


@element_metadata(num_params=2, units=['Ohm', 'sec'])
def K(p, f):
    """ An RC element for use in lin-KK model

    Notes
    -----
    .. math::

        Z = \\frac{R}{1 + j \\omega \\tau_k}

    """
    omega = 2*np.pi*np.array(f)
    R, tau_k = p[0], p[1]
    Z = R/(1 + 1j*omega*tau_k)
    return Z


@element_metadata(num_params=3, units=['Ohm', 'F sec^(gamma - 1)', ''])
def TLMQ(p, f):
    """ Simplified transmission-line model as defined in Eq. 11 of [1]

    Notes
    -----
    .. math::

        Z = \\sqrt{R_{ion}Z_{S}} \\coth \\sqrt{\\frac{R_{ion}}{Z_{S}}


    [1] J. Landesfeind et al.,
    Journal of The Electrochemical Society, 163 (7) A1373-A1387 (2016)
    `doi: 10.1016/10.1149/2.1141607jes
    <http://doi.org/10.1149/2.1141607jes>`_.
    """
    omega = 2*np.pi*np.array(f)
    Rion, Qs, gamma = p[0], p[1], p[2]
    Zs = Qs*(1j*omega)**gamma
    Z = np.sqrt(Rion/Zs)/np.tanh(np.sqrt(Rion*Zs))
    return Z


@element_metadata(num_params=4, units=['Ohm-m^2', 'Ohm-m^2', '', 'sec'])
def T(p, f):
    """ A macrohomogeneous porous electrode model from Paasch et al. [1]

    Notes
    -----
    .. math::

        Z = A\\frac{\\coth{\\beta}}{\\beta} + B\\frac{1}{\\beta\\sinh{\\beta}}

    where

    .. math::

        A = d\\frac{\\rho_1^2 + \\rho_2^2}{\\rho_1 + \\rho_2} \\quad
        B = d\\frac{2 \\rho_1 \\rho_2}{\\rho_1 + \\rho_2}

    and

    .. math::
        \\beta = (a + j \\omega b)^{1/2} \\quad
        a = \\frac{k d^2}{K} \\quad b = \\frac{d^2}{K}


    [1] G. Paasch, K. Micka, and P. Gersdorf,
    Electrochimica Acta, 38, 2653–2662 (1993)
    `doi: 10.1016/0013-4686(93)85083-B
    <https://doi.org/10.1016/0013-4686(93)85083-B>`_.
    """

    omega = 2*np.pi*np.array(f)
    A, B, a, b = p[0], p[1], p[2], p[3]
    beta = (a + 1j*omega*b)**(1/2)

    sinh = []
    for x in beta:
        if x < 100:
            sinh.append(np.sinh(x))
        else:
            sinh.append(1e10)

    Z = A/(beta*np.tanh(beta)) + B/(beta*np.array(sinh))
    return Z


circuit_elements = {key: eval(key) for key in set(globals())-set(initial_state)
                    if key not in non_element_functions}


def get_element_from_name(name):
    excluded_chars = '0123456789_'
    return ''.join(char for char in name if char not in excluded_chars)


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

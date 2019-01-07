import numpy as np
from scipy.optimize import least_squares
from .fitting import rmse


def linKK(f, Z, c=0.85, max_M=50):
    """ A method for implementing the Lin-KK test for validating linearity [1]

    Parameters
    ----------
    f: np.ndarray
        measured frequencies
    Z: np.ndarray of complex numbers
        measured impedances
    c: np.float
        cutoff for mu
    max_M: int
        the maximum number of RC elements

    Returns
    -------
    mu: np.float
        under- or over-fitting measure
    residuals: np.ndarray of complex numbers
        the residuals of the fit at input frequencies
    Z_fit: np.ndarray of complex numbers
        impedance of fit at input frequencies

    Notes
    -----

    The lin-KK method from Schönleber et al. [1] is a quick test for checking
    the
    validity of EIS data. The validity of an impedance spectrum is analyzed by
    its reproducibility by a Kramers-Kronig (KK) compliant equivalent circuit.
    In particular, the model used in the lin-KK test is an ohmic resistor,
    :math:`R_{Ohm}`, and :math:`M` RC elements.

    .. math::

        \\hat Z = R_{Ohm} + \\sum_{k=1}^{M} \\frac{R_k}{1 + j \\omega \\tau_k}

    The :math:`M` time constants, :math:`\\tau_k`, are distributed
    logarithmically,

    .. math::
        \\tau_1 = \\frac{1}{\\omega_{max}} ; \\tau_M = \\frac{1}{\\omega_{min}}
        ; \\tau_k = 10^{\\log{(\\tau_{min}) + \\frac{k-1}{M-1}\\log{{(
            \\frac{\\tau_{max}}{\\tau_{min}}}})}}

    and are not fit during the test (only :math:`R_{Ohm}` and :math:`R_{k}`
    are free parameters).

    In order to prevent under- or over-fitting, Schönleber et al. propose using
    the ratio of positive resistor mass to negative resistor mass as a metric
    for finding the optimal number of RC elements.

    .. math::

        \\mu = 1 - \\frac{\\sum_{R_k \\ge 0} |R_k|}{\\sum_{R_k < 0} |R_k|}

    The argument :code:`c` defines the cutoff value for :math:`\\mu`. The
    algorithm starts at :code:`M = 3` and iterates up to :code:`max_M` until a
    :math:`\\mu < c` is reached. The default of 0.85 is simply a heuristic
    value based off of the experience of Schönleber et al.

    If the argument :code:`c` is :code:`None`, then the automatic determination
    of RC elements is turned off and the solution is calculated for
    :code:`max_M` RC elements. This manual mode should be used with caution as
    under- and over-fitting should be avoided.

    [1] Schönleber, M. et al. A Method for Improving the Robustness of
    linear Kramers-Kronig Validity Tests. Electrochimica Acta 131, 20–27 (2014)
    `doi: 10.1016/j.electacta.2014.01.034
    <https://doi.org/10.1016/j.electacta.2014.01.034>`_.

    """

    def get_tc_distribution(f, M):
        """ Returns the distribution of time constants for the linKK method """

        t_max = 1/np.min(f)
        t_min = 1/np.max(f)

        ts = np.zeros(shape=(M,))
        ts[0] = t_min
        ts[-1] = t_max
        if M > 1:
            for k in range(2, M):
                ts[k-1] = 10**(np.log10(t_min) +
                               ((k-1)/(M-1))*np.log10(t_max/t_min))

        ts *= 2*np.pi

        return ts

    if c is not None:
        M = 0
        mu = 1
        while mu > c and M <= max_M:
            M += 1
            ts = get_tc_distribution(f, M)
            p_values, mu = fitLinKK(f, ts, M, Z)

            if M % 10 == 0:
                print(M, mu, rmse(eval_linKK(p_values, ts, f), Z))
    else:
        M = max_M
        ts = get_tc_distribution(f, M)
        p_values, mu = fitLinKK(f, M, Z)

    return M, mu, eval_linKK(p_values, ts, f), \
        residuals_linKK(p_values, ts, Z, f, residuals='real'), \
        residuals_linKK(p_values, ts, Z, f, residuals='imag')


def fitLinKK(f, ts, M, Z):
    """ Fits the linKK model using scipy.optimize.least_squares """
    initial_guess = np.append(min(np.real(Z)),
                              np.ones(shape=(M,)) *
                              ((max(np.real(Z))-min(np.real(Z)))/M))

    result = least_squares(residuals_linKK, initial_guess, method='lm',
                           args=(ts, Z, f, 'both'),
                           ftol=1E-13, gtol=1E-10)

    p_values = result['x']
    mu = calc_mu(p_values[1:])

    return p_values, mu


def eval_linKK(Rs, ts, f):
    """ Builds a circuit of RC elements to be used in LinKK """
    from .circuit_elements import s, R, K  # noqa

    circuit_string = 's([R({},{}),'.format([Rs[0]], f.tolist())

    for i, (Rk, tk) in enumerate(zip(Rs[1:], ts)):
        circuit_string += 'K({},{}),'.format([Rk, tk], f.tolist())

    circuit_string = circuit_string.strip(',')
    circuit_string += '])'

    return eval(circuit_string)


def residuals_linKK(Rs, ts, Z, f, residuals='real'):
    """ Calculates the residual between the data and a LinKK fit """

    err = Z - eval_linKK(Rs, ts, f)

    if residuals == 'real':
        return err.real/(np.abs(Z))
    elif residuals == 'imag':
        return err.imag/(np.abs(Z))
    elif residuals == 'both':
        z1d = np.zeros(Z.size*2, dtype=np.float64)
        z1d[0:z1d.size:2] = err.real/(np.abs(Z))
        z1d[1:z1d.size:2] = err.imag/(np.abs(Z))

        return z1d


def calc_mu(Rs):
    """ Calculates mu for use in LinKK """

    neg_sum = sum(abs(x) for x in Rs if x < 0)
    pos_sum = sum(abs(x) for x in Rs if x >= 0)

    return 1 - neg_sum/pos_sum

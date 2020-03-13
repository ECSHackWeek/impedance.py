from impedance.validation import calc_mu, eval_linKK, residuals_linKK
import numpy as np


def test_eval_linKK():

    R0 = 1
    Rs = [1, 2]
    ts = [.1, .2]
    f = np.array([.01, 1000])
    w = 2 * np.pi * f

    Z = R0 + (Rs[0]/(1 + ts[0]*1j*w)) + (Rs[1]/(1 + ts[1]*1j*w))

    assert (eval_linKK(Rs, R0, ts, f) == Z).all()

    Z_data = Z + np.array([1 + 1j, 1 + 1j])

    assert (residuals_linKK(Rs, R0, ts, Z_data, f) ==
            (Z_data - Z).real/np.abs(Z_data)).all()

    assert (residuals_linKK(Rs, R0, ts, Z_data, f, residuals='imag') ==
            (Z_data - Z).imag/np.abs(Z_data)).all()

    diff_real = (Z_data - Z).real/np.abs(Z_data)
    diff_imag = (Z_data - Z).imag/np.abs(Z_data)
    assert (residuals_linKK(Rs, R0, ts, Z_data, f, residuals='both') ==
            [diff_real[0], diff_imag[0], diff_real[1], diff_imag[1]]).all()


def test_calc_mu():
    Rs = [1, 2, 3, -3, -2, -1]
    assert calc_mu(Rs) == 0

    Rs = [-1, 2, 4, -3, 4, -1]
    assert calc_mu(Rs) == 0.5

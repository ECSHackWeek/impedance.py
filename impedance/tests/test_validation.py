from impedance.validation import rmse
import numpy as np


def test_RMSE():
    a = np.array([2 + 4*1j, 3 + 2*1j])
    b = np.array([2 + 4*1j, 3 + 2*1j])

    assert rmse(a, b) == 0.0

    c = np.array([2 + 4*1j, 1 + 4*1j])
    d = np.array([4 + 2*1j, 3 + 2*1j])

    assert rmse(c, d) == 2*np.sqrt(2)

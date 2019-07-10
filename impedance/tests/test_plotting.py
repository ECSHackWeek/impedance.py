import os
import numpy as np
from impedance.plotting import plot_nyquist

import matplotlib as mpl
if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt  # noqa E402


def test_plot_nyquist():

    frequencies = [1000.0, 1.0, 0.01]
    Z = np.array([1, 2, 3]) + 1j*np.array([2, 3, 4])

    _, ax = plt.subplots()
    ax = plot_nyquist(ax, frequencies, Z)

    xs, ys = ax.lines[0].get_xydata().T

    assert (xs == Z.real).all() and (ys == -Z.imag).all()

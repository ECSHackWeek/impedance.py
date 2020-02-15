import matplotlib.pyplot as plt  # noqa E402
import numpy as np
from impedance.plotting import plot_nyquist


def test_plot_nyquist():

    Z = np.array([1, 2, 3]) + 1j*np.array([2, 3, 4])

    _, ax = plt.subplots()
    ax = plot_nyquist(ax, Z)

    xs, ys = ax.lines[0].get_xydata().T

    assert (xs == Z.real).all() and (ys == -Z.imag).all()

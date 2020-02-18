import matplotlib.pyplot as plt  # noqa E402
import numpy as np
from impedance.plotting import plot_altair, plot_bode, plot_nyquist
import json


def test_plot_bode():

    f = [1, 10, 100]
    Z = np.array([1, 2, 3]) + 1j*np.array([2, 3, 4])

    _, axes = plt.subplots(nrows=2)
    axes = plot_bode(axes, f, Z)

    xs, ys = axes[0].lines[0].get_xydata().T
    assert (xs == f).all() and (ys == np.abs(Z)).all()

    xs, ys = axes[1].lines[0].get_xydata().T
    assert (xs == f).all() and (ys == -np.angle(Z, deg=True)).all()


def test_plot_nyquist():

    Z = np.array([1, 2, 3]) + 1j*np.array([2, 3, 4])

    _, ax = plt.subplots()
    ax = plot_nyquist(ax, Z)

    xs, ys = ax.lines[0].get_xydata().T

    assert (xs == Z.real).all() and (ys == -Z.imag).all()


def test_plot_altair():
    frequencies = [1000.0, 1.0, 0.01]
    Z = np.array([1, 2, 3]) + 1j*np.array([2, 3, 4])

    chart = plot_altair({'data': {'f': frequencies, 'Z': Z},
                         'fit': {'f': frequencies, 'Z': Z, 'fmt': '-'}},
                        size=400)

    datasets = json.loads(chart.to_json())['datasets']
    for dataset in datasets.keys():
        assert len(datasets[dataset]) == len(Z)

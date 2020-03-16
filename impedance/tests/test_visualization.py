import matplotlib.pyplot as plt
import numpy as np
from impedance.visualization import plot_altair, plot_bode, plot_nyquist
from impedance.visualization import plot_residuals
import json


def test_plot_bode():

    f = [1, 10, 100]
    Z = np.array([1, 2, 3]) + 1j*np.array([2, 3, 4])

    _, axes = plt.subplots(nrows=2)
    axes = plot_bode(axes, f, Z, scale=10)

    xs, ys = axes[0].lines[0].get_xydata().T
    assert (xs == f).all() and (ys == np.abs(Z)).all()

    xs, ys = axes[1].lines[0].get_xydata().T
    assert (xs == f).all() and (ys == -np.angle(Z, deg=True)).all()


def test_plot_nyquist():

    Z = np.array([1, 2, 3]) + 1j*np.array([2, 3, 4])

    _, ax = plt.subplots()
    ax = plot_nyquist(ax, Z, scale=10)

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


def test_plot_residuals():

    f = [1, 10, 100]
    res_real = np.array([1, 2, 3])
    res_imag = np.array([2, 3, 4])

    _, ax = plt.subplots()
    ax = plot_residuals(ax, f, res_real, res_imag)

    xs, ys = ax.lines[0].get_xydata().T
    # Multiply x100 because plots are %
    assert (xs == f).all() and (ys == res_real * 100).all()

    xs, ys = ax.lines[1].get_xydata().T
    assert (xs == f).all() and (ys == res_imag * 100).all()

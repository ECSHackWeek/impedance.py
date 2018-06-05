from impedance.fitting import buildCircuit, rmse
import numpy as np

# def test_residuals():
#     pass
#
#
# def test_valid():
#     pass
#
#
# def test_computeCircuit():
#     pass


def test_buildCircuit():

    circuit = 'R_0-p(R_1, E_1/E_2)-W_1/W_2'
    parameters = [.1, .01, 15, .9, 1, 1000]
    frequencies = [1000.0, 1.0, 0.01]

    assert buildCircuit(circuit, parameters, frequencies).replace(' ', '') == \
        's([R([0.1],[1000.0,1.0,0.01]),' + \
        'p((R([0.01],[1000.0,1.0,0.01]),' + \
        '([15,0.9],[1000.0,1.0,0.01]))),' + \
        'W([1,1000],[1000.0,1.0,0.01])])'


def test_RMSE():
    a = np.array([2 + 4*1j, 3 + 2*1j])
    b = np.array([2 + 4*1j, 3 + 2*1j])

    assert rmse(a, b) == 0.0

    c = np.array([2 + 4*1j, 1 + 4*1j])
    d = np.array([4 + 2*1j, 3 + 2*1j])

    assert rmse(c, d) == 2*np.sqrt(2)

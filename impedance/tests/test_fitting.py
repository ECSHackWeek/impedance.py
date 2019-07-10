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

    # Test simple Randles circuit with CPE
    circuit = 'R_0-p(R_1, E_1)-W_1'
    params = [.1, .01, 15, .9, 1, 1000]
    frequencies = [1000.0, 5.0, 0.01]

    assert buildCircuit(circuit, frequencies, *params)[0].replace(' ', '') == \
        's([R([0.1],[1000.0,5.0,0.01]),' + \
        'p([R([0.01],[1000.0,5.0,0.01]),' + \
        'E([15.0,0.9],[1000.0,5.0,0.01])]),' + \
        'W([1.0,1000.0],[1000.0,5.0,0.01])])'

    # Test multiple parallel elements
    circuit = 'R_0-p(C_1,R_1,R_2)'
    params = [.1, .01, .2, .3]
    frequencies = [1000.0, 5.0, 0.01]

    assert buildCircuit(circuit, frequencies, *params)[0].replace(' ', '') == \
        's([R([0.1],[1000.0,5.0,0.01]),' + \
        'p([C([0.01],[1000.0,5.0,0.01]),' + \
        'R([0.2],[1000.0,5.0,0.01]),' + \
        'R([0.3],[1000.0,5.0,0.01])])])'

    # Test nested parallel groups
    circuit = 'R_0-p(p(R_1, C_1)-R_2, C_2)'
    params = [1, 2, 3, 4, 5]
    frequencies = [1000.0, 5.0, 0.01]

    assert buildCircuit(circuit, frequencies, *params)[0].replace(' ', '') == \
        's([R([1],[1000.0,5.0,0.01]),' + \
        'p([s([p([R([2],[1000.0,5.0,0.01]),' + \
        'C([3],[1000.0,5.0,0.01])]),' + \
        'R([4],[1000.0,5.0,0.01])]),' + \
        'C([5],[1000.0,5.0,0.01])])])'


def test_RMSE():
    a = np.array([2 + 4*1j, 3 + 2*1j])
    b = np.array([2 + 4*1j, 3 + 2*1j])

    assert rmse(a, b) == 0.0

    c = np.array([2 + 4*1j, 1 + 4*1j])
    d = np.array([4 + 2*1j, 3 + 2*1j])
    assert np.isclose(rmse(c, d), 2*np.sqrt(2))

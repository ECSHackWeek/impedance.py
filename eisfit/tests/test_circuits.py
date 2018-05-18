from EISfit.circuits import Randles
import numpy as np

# store some global test data
data = np.genfromtxt('./tests/Z1tofit.csv', delimiter=',')
frequencies = data[:, 0]
Z = data[:, 1] + 1j*data[:, 2]


def test_Randles():
    # check for proper functionality
    global frequencies, Z
    r = Randles(initial_guess=[.01, .005, .1, .0001, 200])
    r.fit(frequencies[np.imag(Z) < 0], Z[np.imag(Z) < 0])
    np.testing.assert_almost_equal(r.parameters_,
                                   np.array([1.86146620e-02, 1.15477171e-02,
                                             1.33331949e+00, 6.31473571e-02,
                                             2.22407275e+02]), decimal=2)

    # check that it rejects improper inputs - enforcing initial guess types
    try:
        r = Randles(initial_guess=['hi', 0.1])
    except(AssertionError):
        pass
    else:
        raise Exception('unhandled error occurred')

    # check that it rejects improper inputs - enforcing data types
    try:
        r = Randles(initial_guess=[.01, .005, .1, .0001, 200])
        r.fit(['hi', 'hello'], [0.5, 0.2])
    except(AssertionError):
        pass
    else:
        raise Exception('unhandled error occurred')

    # check that it rejects improper inputs - enforcing data lengths
    try:
        r = Randles(initial_guess=[.01, .005, .1, .0001, 200])
        r.fit(frequencies[np.imag(Z) < 0][:5], Z[np.imag(Z) < 0])
    except(AssertionError):
        pass
    else:
        raise Exception('unhandled error occurred')

    # check that it rejects improper inputs
    # enforcing the length of initial_guess
    try:
        r = Randles(initial_guess=[.01, .005, .1, .0001])
    except(AssertionError):
        pass
    else:
        raise Exception('unhandled error occurred')

    return


def test_BaseCircuit():
    pass

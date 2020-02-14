from impedance.circuits import BaseCircuit, CustomCircuit, Randles
import matplotlib.pyplot as plt
import numpy as np


def test_BaseCircuit():

    initial_guess = [0.01, 0.02, 50]
    base_circuit = BaseCircuit(initial_guess)

    assert base_circuit.initial_guess == initial_guess


def test_Randles():
    # check for proper functionality

    # get example data
    data = np.genfromtxt('./data/exampleData.csv', delimiter=',')

    frequencies = data[:, 0]
    Z = data[:, 1] + 1j*data[:, 2]

    randles = Randles(initial_guess=[.01, .005, .1, .0001, 200])
    randles.fit(frequencies[np.imag(Z) < 0], Z[np.imag(Z) < 0])
    np.testing.assert_almost_equal(randles.parameters_,
                                   np.array([1.86146620e-02, 1.15477171e-02,
                                             1.33331949e+00, 6.31473571e-02,
                                             2.22407275e+02]), decimal=2)

    # check that plotting returns a plt.Axes() object
    _, ax = plt.subplots()
    assert isinstance(randles.plot(ax, frequencies, Z), type(ax))
    assert isinstance(randles.plot(ax, frequencies, Z,
                                   conf_bounds='error_bars'), type(ax))

    # check that predicting impedance from fit works
    assert np.isclose(randles.predict(np.array([10.0])),
                      np.complex(0.02495749, -0.00614842))

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

    # check that it rejects missing input
    try:
        r = Randles()
    except(TypeError):
        pass
    else:
        raise Exception('unhandled error occured')

    return


def test_CustomCircuit():

    initial_guess = [.01, .005, .1, .005, .1, .001, 200]
    custom_string = 'R0-p(R1,C1)-p(R2,C2)-W1'
    custom_circuit = CustomCircuit(initial_guess=initial_guess,
                                   circuit=custom_string)

    # check get_param_names()
    full_names, all_units = custom_circuit.get_param_names()
    assert full_names == ['R0', 'R1', 'C1', 'R2', 'C2', 'W1_0', 'W1_1']
    assert all_units == ['Ohm', 'Ohm', 'F', 'Ohm', 'F', 'Ohm', 'sec']

    # check _is_fit()
    assert not custom_circuit._is_fit()

    initial_guess = [.01, .005, .1]
    custom_string = 'R0-p(R1,C1)'
    custom_circuit = CustomCircuit(initial_guess=initial_guess,
                                   circuit=custom_string, name='Test')

    assert str(custom_circuit) == \
        '\nName: Test\n' + \
        'Circuit string: R0-p(R1,C1)\n' + \
        'Fit: False\n' + \
        '\nInitial guesses:\n' + \
        '     R0 = 1.00e-02 [Ohm]\n' + \
        '     R1 = 5.00e-03 [Ohm]\n' + \
        '     C1 = 1.00e-01 [F]\n'

    # check that it rejects improper inputs
    # enforcing the length of initial_guess
    try:
        initial_guess = [.01, .005, .1, .005, .1, .001, 200]
        custom_string = 'R0-p(R1,E1)-p(R1,C1)-W1'
        custom_circuit = CustomCircuit(initial_guess=initial_guess,
                                       circuit=custom_string)
    except(AssertionError):
        pass
    else:
        raise Exception('unhandled error occurred')

    return

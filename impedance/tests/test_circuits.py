from impedance.models.circuits import BaseCircuit, CustomCircuit, Randles
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pytest

# get example data
data = np.genfromtxt(os.path.join("./data/",
                                  "exampleData.csv"), delimiter=',')

f = data[:, 0]
Z = data[:, 1] + 1j * data[:, 2]


def test_BaseCircuit():
    initial_guess = [0.01, 0.02, 50]
    base_circuit = BaseCircuit(initial_guess)

    # check that initial_guess is loaded in correctly
    assert base_circuit.initial_guess == initial_guess

    # check that plotting returns a plt.Axes() object
    _, ax = plt.subplots()
    assert isinstance(base_circuit.plot(ax, None, Z, kind='nyquist'), type(ax))
    assert isinstance(base_circuit.plot(None, f, Z, kind='nyquist'), type(ax))
    _, axes = plt.subplots(nrows=2)
    assert isinstance(base_circuit.plot(axes, f, Z, kind='bode')[0], type(ax))
    assert isinstance(base_circuit.plot(None, f, Z, kind='bode')[0], type(ax))

    with pytest.raises(ValueError):
        base_circuit.plot(None, f, Z, kind='SomethingElse')

    # check that it rejects improper inputs - enforcing initial guess types
    with pytest.raises(AssertionError):
        r = BaseCircuit(initial_guess=['hi', 0.1])

    # check that it rejects improper inputs - enforcing data types
    with pytest.raises(AssertionError):
        r = BaseCircuit(initial_guess=[.01, .005, .1, .0001, 200])
        r.fit(['hi', 'hello'], [0.5, 0.2])

    # check that it raises TypeError if incorrectly compared
    with pytest.raises(TypeError):
        r = BaseCircuit(initial_guess=[.01, .005, .1, .0001, 200])
        r == 8


def test_Randles():
    randles = Randles(initial_guess=[.01, .005, .1, .0001, 200])
    randles.fit(f[np.imag(Z) < 0], Z[np.imag(Z) < 0])
    np.testing.assert_almost_equal(randles.parameters_,
                                   np.array([1.86146620e-02, 1.15477171e-02,
                                             1.33331949e+00, 6.31473571e-02,
                                             2.22407275e+02]), decimal=2)

    # check altair plotting with a fit circuit
    chart = randles.plot(f_data=f, Z_data=Z)
    datasets = json.loads(chart.to_json())['datasets']
    for dataset in datasets.keys():
        assert len(datasets[dataset]) == len(Z)

    # check defaults work if no frequency data is passed
    chart = randles.plot(Z_data=Z)

    # bode plots
    randles.plot(f_data=f, Z_data=Z, kind='bode')
    with pytest.raises(AssertionError):
        randles.plot(Z_data=Z, kind='bode')

    # nyquist plots
    randles.plot(f_data=f, Z_data=Z, kind='nyquist')
    randles.plot(Z_data=Z, kind='nyquist')

    # check that predicting impedance from fit works
    assert np.isclose(randles.predict(np.array([10.0])),
                      np.complex(0.02495749, -0.00614842))

    # check that equality comparisons work
    randles1 = Randles(initial_guess=[.01, .005, .1, .0001, 200])
    randles2 = Randles(initial_guess=[.01, .005, .1, .0001, 200])

    assert randles1 == randles2

    randles1.fit(f[np.imag(Z) < 0], Z[np.imag(Z) < 0])
    assert randles1 != randles2

    randles2.fit(f[np.imag(Z) < 0], Z[np.imag(Z) < 0])
    assert randles1 == randles2

    randles2.fit(f, Z)
    assert randles1 != randles2

    randles = Randles(initial_guess=[.01, .005, .1, 0.9, .0001, 200], CPE=True)


def test_CustomCircuit():
    initial_guess = [.01, .005, .1, .005, .1, .001, 200]
    custom_string = 'R0-p(R1,C1)-p(R2,C2)-Wo1'
    custom_circuit = CustomCircuit(initial_guess=initial_guess,
                                   circuit=custom_string)

    # check get_param_names()
    full_names, all_units = custom_circuit.get_param_names()
    assert full_names == ['R0', 'R1', 'C1', 'R2', 'C2', 'Wo1_0', 'Wo1_1']
    assert all_units == ['Ohm', 'Ohm', 'F', 'Ohm', 'F', 'Ohm', 'sec']

    # check _is_fit()
    assert not custom_circuit._is_fit()

    # check predictions from initial_guesses
    high_f = np.array([1e9])
    assert np.isclose(np.real(custom_circuit.predict(high_f)[0]),
                      initial_guess[0])

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

    customConstantCircuit = CustomCircuit(initial_guess=[None, .005, .1, .005, .1, .001, None],
                                            constants={'R_0': 0.02, 'Wo_1_1': 200},
                                            circuit='R_0-p(R_1,C_1)-p(R_2,C_2)-Wo_1')
    print(customConstantCircuit)

    initial_guess = [.01, .005, .1]
    custom_string = 'R0-p(R1,C1)'
    custom_circuit = CustomCircuit(initial_guess=initial_guess,
                                   circuit=custom_string)
    custom_circuit.fit(f, Z)
    custom_circuit.plot(f_data=f, Z_data=Z)

    with pytest.raises(AssertionError):
        initial_guess = [.01, .005, .1, .005, .1, .001, 200]
        custom_string = 'R0-p(R1,CPE1)-p(R1,C1)-Wo1'
        custom_circuit = CustomCircuit(initial_guess=initial_guess,
                                       circuit=custom_string)

    with pytest.raises(ValueError):
        custom_circuit = CustomCircuit()
        custom_circuit.fit(f, Z)

    with pytest.raises(ValueError):
        custom_circuit = CustomCircuit('R0-NotAnElement', initial_guess=[1, 2])

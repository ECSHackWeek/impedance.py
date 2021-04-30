import json
import os

import numpy as np
import matplotlib.pyplot as plt
import pytest

from impedance.models.circuits import BaseCircuit, CustomCircuit, Randles

# get example data
data = np.genfromtxt(os.path.join("./data/",
                                  "exampleData.csv"), delimiter=',')

f = data[:, 0]
Z = data[:, 1] + 1j * data[:, 2]


def test_BaseCircuit():
    initial_guess = [0.01, 0.02, 50]
    base_circuit = BaseCircuit(initial_guess)

    # __init__()
    # check initial_guess is loaded in correctly
    assert base_circuit.initial_guess == initial_guess

    # improper input_guess types raise an TypeError
    with pytest.raises(TypeError):
        r = BaseCircuit(initial_guess=['hi', 0.1])

    # __eq__()
    # incorrect comparisons raise a TypeError
    with pytest.raises(TypeError):
        r = BaseCircuit(initial_guess=[.01, .005, .1, .0001, 200])
        r == 8

    # fit()
    # improper data types in fitting raise a TypeError
    with pytest.raises(TypeError):
        r = BaseCircuit(initial_guess=[.01, .005, .1, .0001, 200])
        r.fit([42, 4.2], [])  # frequencies not ndarray

    with pytest.raises(TypeError):
        r = BaseCircuit(initial_guess=[.01, .005, .1, .0001, 200])
        r.fit(np.array([42 + 42j]), [])  # frequencies not numeric type

    with pytest.raises(TypeError):
        r = BaseCircuit(initial_guess=[.01, .005, .1, .0001, 200])
        r.fit(np.array([42]), [42 + 42j])  # Z not ndarray

    with pytest.raises(TypeError):
        r = BaseCircuit(initial_guess=[.01, .005, .1, .0001, 200])
        r.fit(np.array([42]), np.array([0.5, 0.2]))  # Z not complex

    with pytest.raises(TypeError):
        r = BaseCircuit(initial_guess=[.01, .005, .1, .0001, 200])
        r.fit(np.array([42, 4.2]), np.array([42 + 42j]))  # mismatched lengths

    # predict()
    # improper data types in fitting raise a TypeError
    with pytest.raises(TypeError):
        r = BaseCircuit(initial_guess=[.01, .005, .1, .0001, 200])
        r.predict([42, 4.2])  # frequencies not ndarray

    with pytest.raises(TypeError):
        r = BaseCircuit(initial_guess=[.01, .005, .1, .0001, 200])
        r.predict(np.array([42 + 42j]))  # frequencies not numeric type

    # plot()
    # kind = {'nyquist', 'bode'} should return a plt.Axes() object
    _, ax = plt.subplots()
    assert isinstance(base_circuit.plot(ax, None, Z, kind='nyquist'), type(ax))
    assert isinstance(base_circuit.plot(None, f, Z, kind='nyquist'), type(ax))
    _, axes = plt.subplots(nrows=2)
    assert isinstance(base_circuit.plot(axes, f, Z, kind='bode')[0], type(ax))
    assert isinstance(base_circuit.plot(None, f, Z, kind='bode')[0], type(ax))

    # incorrect kind raises a ValueError
    with pytest.raises(ValueError):
        base_circuit.plot(None, f, Z, kind='SomethingElse')


def test_Randles():
    randles = Randles(initial_guess=[.01, .005, .1, .01, 200])
    randlesCPE = Randles(initial_guess=[.01, .05, .1, 0.9, .01, 200], CPE=True)
    with pytest.raises(ValueError):
        randlesCPE = Randles([.01, 200])  # incorrect initial guess length
    randles.fit(f[np.imag(Z) < 0], Z[np.imag(Z) < 0])
    randlesCPE.fit(f[np.imag(Z) < 0], Z[np.imag(Z) < 0])

    # compare with known fit parameters
    np.testing.assert_almost_equal(randles.parameters_,
                                   np.array([1.86146620e-02, 1.15477171e-02,
                                             1.33331949e+00, 6.31473571e-02,
                                             2.22407275e+02]), decimal=2)

    # compare with known impedance predictions
    assert np.isclose(randles.predict(np.array([10.0])),
                      np.complex(0.02495749, -0.00614842))

    # check altair plotting with a fit circuit
    chart = randles.plot(f_data=f, Z_data=Z)
    datasets = json.loads(chart.to_json())['datasets']
    for dataset in datasets.keys():
        assert len(datasets[dataset]) == len(Z)

    # plot() with fitted model
    # check defaults work if no frequency data is passed
    chart = randles.plot(Z_data=Z)

    # bode plots
    randles.plot(f_data=f, Z_data=Z, kind='bode')
    randles.plot(kind='bode')
    with pytest.raises(ValueError):
        randles.plot(Z_data=Z, kind='bode')  # missing f_data

    # nyquist plots
    randles.plot(f_data=f, Z_data=Z, kind='nyquist')
    randles.plot(Z_data=Z, kind='nyquist')

    # check equality comparisons work
    randles1 = Randles(initial_guess=[.01, .005, .1, .0001, 200])
    randles2 = Randles(initial_guess=[.01, .005, .1, .0001, 200])
    assert randles1 == randles2

    randles1.fit(f[np.imag(Z) < 0], Z[np.imag(Z) < 0])
    assert randles1 != randles2

    randles2.fit(f[np.imag(Z) < 0], Z[np.imag(Z) < 0])
    assert randles1 == randles2

    randles2.fit(f, Z)
    assert randles1 != randles2


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

    # __str()__
    initial_guess = [.01, .005, .1]
    custom_string = 'R0-p(R1,C1)'
    custom_circuit = CustomCircuit(initial_guess=initial_guess,
                                   circuit=custom_string)

    assert str(custom_circuit) == \
        '\nCircuit string: R0-p(R1,C1)\n' + \
        'Fit: False\n' + \
        '\nInitial guesses:\n' + \
        '     R0 = 1.00e-02 [Ohm]\n' + \
        '     R1 = 5.00e-03 [Ohm]\n' + \
        '     C1 = 1.00e-01 [F]\n'

    custom_circuit.fit(f, Z)
    assert custom_circuit._is_fit()
    custom_circuit.plot(f_data=f, Z_data=Z)

    # constants and _ in circuit and no name
    circuit = 'R_0-p(R_1,C_1)-Wo_1'
    constants = {'R_0': 0.02, 'Wo_1_1': 200}
    initial_guess = [.005, .1, .001]
    custom_circuit = CustomCircuit(initial_guess=initial_guess,
                                   constants=constants, circuit=circuit,
                                   name='Test')

    assert str(custom_circuit) == \
        '\nName: Test\n' + \
        'Circuit string: R_0-p(R_1,C_1)-Wo_1\n' + \
        'Fit: False\n' + \
        '\nConstants:\n' + \
        '    R_0 = 2.00e-02 [Ohm]\n' + \
        '  Wo_1_1 = 2.00e+02 [sec]\n' + \
        '\nInitial guesses:\n' + \
        '    R_1 = 5.00e-03 [Ohm]\n' + \
        '    C_1 = 1.00e-01 [F]\n' + \
        '  Wo_1_0 = 1.00e-03 [Ohm]\n'

    # incorrect number of initial guesses
    with pytest.raises(ValueError):
        initial_guess = [.01, .005, .1, .005, .1, .001, 200]
        custom_string = 'R0-p(R1,CPE1)-p(R1,C1)-Wo1'
        custom_circuit = CustomCircuit(initial_guess=initial_guess,
                                       circuit=custom_string)

    # no initial guesses supplied before fitting
    with pytest.raises(ValueError):
        custom_circuit = CustomCircuit()
        custom_circuit.fit(f, Z)

    # incorrect circuit element in circuit
    with pytest.raises(ValueError):
        custom_circuit = CustomCircuit('R0-NotAnElement', initial_guess=[1, 2])

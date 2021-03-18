from impedance.preprocessing import ignoreBelowX
from impedance.models.circuits.fitting import buildCircuit, \
    circuit_fit, rmse, extract_circuit_elements
from impedance.tests.test_preprocessing import frequencies \
    as example_frequencies
from impedance.tests.test_preprocessing import Z_correct

import numpy as np

# def test_residuals():
#     pass
#
#
# def test_valid():
#     pass
#
#


def test_circuit_fit():

    # Test example circuit from "Getting Started" page
    circuit = 'R0-p(R1,C1)-p(R2-Wo1,C2)'
    initial_guess = [.01, .01, 100, .01, .05, 100, 1]
    results_local = np.array([1.65e-2, 8.68e-3, 3.32e0, 5.39e-3,
                              6.31e-2, 2.33e2, 2.20e-1])
    results_global = np.array([1.65e-2, 5.34e-3, 0.22, 9.15e-3,
                               1.31e-1, 1.10e3, 2.78])

    # Filter
    example_frequencies_filtered, \
        Z_correct_filtered = ignoreBelowX(example_frequencies, Z_correct)

    # Test local fitting
    assert np.isclose(circuit_fit(example_frequencies_filtered,
                                  Z_correct_filtered, circuit,
                                  initial_guess, constants={})[0],
                      results_local, rtol=1e-2).all()

    # Test global fitting on multiple seeds
    # All seeds should converge to the same value
    # seed = 0
    assert np.isclose(circuit_fit(example_frequencies_filtered,
                                  Z_correct_filtered, circuit,
                                  initial_guess, constants={},
                                  global_opt=True, seed=0)[0],
                      results_global, rtol=1e-1).all()

    # seed = 1
    assert np.isclose(circuit_fit(example_frequencies_filtered,
                                  Z_correct_filtered, circuit,
                                  initial_guess, constants={},
                                  global_opt=True, seed=1)[0],
                      results_global, rtol=1e-1).all()

    # seed = 42
    assert np.isclose(circuit_fit(example_frequencies_filtered,
                                  Z_correct_filtered, circuit,
                                  initial_guess, constants={},
                                  global_opt=True, seed=42)[0],
                      results_global, rtol=1e-1).all()


def test_buildCircuit():

    # Test simple Randles circuit with CPE
    circuit = 'R0-p(R1-Wo1,CPE1)'
    params = [.1, .01, 1, 1000, 15, .9]
    frequencies = [1000.0, 5.0, 0.01]

    assert buildCircuit(circuit, frequencies, *params,
                        constants={})[0].replace(' ', '') == \
        's([R([0.1],[1000.0,5.0,0.01]),' + \
        'p([s([R([0.01],[1000.0,5.0,0.01]),' + \
        'Wo([1.0,1000.0],[1000.0,5.0,0.01])]),' + \
        'CPE([15.0,0.9],[1000.0,5.0,0.01])])])'

    # Test multiple parallel elements
    circuit = 'R0-p(C1,R1,R2)'
    params = [.1, .01, .2, .3]
    frequencies = [1000.0, 5.0, 0.01]

    assert buildCircuit(circuit, frequencies, *params,
                        constants={})[0].replace(' ', '') == \
        's([R([0.1],[1000.0,5.0,0.01]),' + \
        'p([C([0.01],[1000.0,5.0,0.01]),' + \
        'R([0.2],[1000.0,5.0,0.01]),' + \
        'R([0.3],[1000.0,5.0,0.01])])])'

    # Test nested parallel groups
    circuit = 'R0-p(p(R1, C1)-R2, C2)'
    params = [1, 2, 3, 4, 5]
    frequencies = [1000.0, 5.0, 0.01]

    assert buildCircuit(circuit, frequencies, *params,
                        constants={})[0].replace(' ', '') == \
        's([R([1],[1000.0,5.0,0.01]),' + \
        'p([s([p([R([2],[1000.0,5.0,0.01]),' + \
        'C([3],[1000.0,5.0,0.01])]),' + \
        'R([4],[1000.0,5.0,0.01])]),' + \
        'C([5],[1000.0,5.0,0.01])])])'

    # Test parallel elements at beginning and end
    circuit = 'p(C1,R1)-p(C2,R2)'
    params = [.1, .01, .2, .3]
    frequencies = [1000.0, 5.0, 0.01]

    assert buildCircuit(circuit, frequencies, *params,
                        constants={})[0].replace(' ', '') == \
        's([p([C([0.1],[1000.0,5.0,0.01]),' + \
        'R([0.01],[1000.0,5.0,0.01])]),' + \
        'p([C([0.2],[1000.0,5.0,0.01]),' + \
        'R([0.3],[1000.0,5.0,0.01])])])'

    # Test single element circuit
    circuit = 'R1'
    params = [100]
    frequencies = [1000.0, 5.0, 0.01]

    assert buildCircuit(circuit, frequencies, *params,
                        constants={})[0].replace(' ', '') == \
        '([R([100],[1000.0,5.0,0.01])])'


def test_RMSE():
    a = np.array([2 + 4*1j, 3 + 2*1j])
    b = np.array([2 + 4*1j, 3 + 2*1j])

    assert rmse(a, b) == 0.0

    c = np.array([2 + 4*1j, 1 + 4*1j])
    d = np.array([4 + 2*1j, 3 + 2*1j])
    assert np.isclose(rmse(c, d), 2*np.sqrt(2))


def test_element_extraction():
    circuit = 'R0-p(RR0,C1)-p(R1,C2032478)-W1'
    extracted_elements = extract_circuit_elements(circuit)
    assert extracted_elements == ['R0', 'RR0', 'C1', 'R1', 'C2032478', 'W1']

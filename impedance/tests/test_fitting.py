from impedance.preprocessing import ignoreBelowX
from impedance.models.circuits.fitting import (
    circuit_fit,
    rmse,
    extract_circuit_elements,
    set_default_bounds,
    objective_function,
    CircuitGraph,
    BoundsCheck,
)
from impedance.tests.test_preprocessing import (
    frequencies as example_frequencies,
)
from impedance.tests.test_preprocessing import Z_correct

import numpy as np
import pytest


def test_set_default_bounds():
    # Test example circuit from "Getting Started" page
    circuit = "R0-p(R1,C1)-p(R2-Wo1,C2)"

    # Test with no constants
    default_bounds = (np.zeros(7), np.inf * np.ones(7))
    bounds_from_func = set_default_bounds(circuit)

    assert np.allclose(default_bounds, bounds_from_func)

    # Test with constants
    constants = {"R0": 1}
    default_bounds = (np.zeros(6), np.inf * np.ones(6))
    bounds_from_func = set_default_bounds(circuit, constants=constants)

    assert np.allclose(default_bounds, bounds_from_func)

    # Test with CPEs
    circuit = "R0-p(R1,CPE1)-p(R2-CPE2)"
    default_bounds = (np.zeros(7), np.inf * np.ones(7))
    default_bounds[1][3] = 1
    default_bounds[1][6] = 1
    bounds_from_func = set_default_bounds(circuit)

    assert np.allclose(default_bounds, bounds_from_func)


def test_circuit_fit():
    # Test trivial model (10 Ohm resistor)
    circuit = "R0"
    initial_guess = [10]

    results_simple = [10]

    frequencies = np.array([10, 100, 1000])
    Z_data = np.array([10, 10, 10])  # impedance is real

    assert np.allclose(
        circuit_fit(
            frequencies,
            Z_data,
            circuit,
            initial_guess,
            constants={},
            global_opt=True,
        )[0],
        results_simple,
        rtol=1e-1,
    )

    # check that list inputs work
    frequency_list = [10, 100, 1000]
    Z_data_list = [10, 10, 10]

    assert np.allclose(
        circuit_fit(
            frequency_list,
            Z_data_list,
            circuit,
            initial_guess,
            constants={},
            global_opt=True,
        )[0],
        results_simple,
        rtol=1e-1,
    )

    # Test example circuit from "Getting Started" page
    circuit = "R0-p(R1,C1)-p(R2-Wo1,C2)"
    initial_guess = [0.01, 0.01, 1, 0.001, 0.1, 100, 0.1]
    bounds = [(0, 0, 0, 0, 0, 0, 0), (10, 1, 1e3, 1, 1, 1e4, 100)]

    # results change slightly using predefined bounds
    results_local = np.array(
        [1.65e-2, 8.78e-3, 3.41, 5.45e-3, 1.43e-1, 1.30e3, 2.23e-1]
    )
    results_local_bounds = results_local.copy()
    results_local_weighted = np.array(
        [1.64e-2, 9.06e-3, 3.06, 5.29e-3, 1.45e-1, 1.32e3, 2.02e-1]
    )

    results_minimize = np.array(
        [1.65e-2, 8.67e-3, 3.32, 5.39e-3, 6.37e-2, 2.38e2, 2.20e-1]
    )
    results_powell = np.array(
        [1.65e-2, 8.69e-3, 3.31, 5.39e-3, 6.45e-2, 2.45e2, 2.19e-1]
    )
    results_global = np.array(
        [1.65e-2, 8.68e-03, 3.32, 5.39e-3, 6.37e-2, 2.38e2, 2.20e-1]
    )

    # Filter
    example_frequencies_filtered, Z_correct_filtered = ignoreBelowX(
        example_frequencies, Z_correct
    )

    graph = CircuitGraph(circuit)
    sum_sq_error = objective_function(
        graph, example_frequencies_filtered, Z_correct_filtered
    )
    # Test local fitting
    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        constants={},
    )[0]
    assert np.allclose(popt, results_local, rtol=1e-2)
    assert sum_sq_error(popt) < 2e-5

    # Test local fitting with predefined bounds
    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        bounds=bounds,
        constants={},
    )[0]
    assert np.allclose(popt, results_local_bounds, rtol=1e-2)
    assert sum_sq_error(popt) < 2e-5

    # Test local fitting with predefined weights
    # Use abs(Z), stacked in order of (Re, Im) components
    sigma = np.hstack((np.abs(Z_correct_filtered), np.abs(Z_correct_filtered)))
    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        sigma=sigma,
        constants={},
    )[0]
    assert np.allclose(popt, results_local_weighted, rtol=1e-2)
    assert sum_sq_error(popt) < 2e-5

    # Test if using weight_by_modulus=True produces the same results
    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        weight_by_modulus=True,
        constants={},
    )[0]
    assert np.allclose(popt, results_local_weighted, rtol=1e-2)
    assert sum_sq_error(popt) < 2e-5

    # Test if using method "minimize" produces the same results
    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        opt_method="minimize",
        constants={},
    )[0]
    assert np.allclose(popt, results_minimize, rtol=1e-2)
    assert sum_sq_error(popt) < 2e-5

    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        opt_method="minimize",
        constants={},
        method="Powell",
    )[0]
    assert np.allclose(popt, results_powell, rtol=1e-2)
    assert sum_sq_error(popt) < 2e-5

    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        opt_method="minimize",
        constants={},
        method="TNC",
        options={"scale": initial_guess, "maxfun": 10_000},
    )[0]
    assert sum_sq_error(popt) < 1e-4

    # Test global fitting on multiple seeds
    # All seeds should converge to the same parameter values
    # seed = 0 (default)
    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        constants={},
        global_opt=True,
    )[0]
    assert np.allclose(popt, results_global, rtol=1e-1)
    assert sum_sq_error(popt) < 2e-5

    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        constants={},
        global_opt=True,
        minimizer_kwargs={
            "method": "TNC",
            "options": {
                "scale": initial_guess,
                "maxfun": 10_000,
            },
        },
    )[0]
    assert sum_sq_error(popt) < 5e-5

    # seed = 0, with predefined bounds
    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        constants={},
        global_opt=True,
        bounds=bounds,
        seed=0,
    )[0]
    assert np.allclose(popt, results_global, rtol=1e-1)
    assert sum_sq_error(popt) < 2e-5

    # seed = 1
    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        constants={},
        global_opt=True,
        seed=1,
    )[0]
    assert np.allclose(popt, results_global, rtol=1e-1)
    assert sum_sq_error(popt) < 2e-5

    # seed = 42
    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        constants={},
        global_opt=True,
        seed=42,
    )[0]
    assert np.allclose(popt, results_global, rtol=1e-1)
    assert sum_sq_error(popt) < 2e-5

    # Test dual annealing
    popt = circuit_fit(
        example_frequencies_filtered,
        Z_correct_filtered,
        circuit,
        initial_guess,
        constants={},
        global_opt=True,
        opt_method="dual_annealing",
    )[0]
    assert np.allclose(popt, results_minimize, rtol=1e-1)
    assert sum_sq_error(popt) < 5e-5


def test_CircuitGraph():
    # Test simple Randles circuit with CPE
    circuit = "R0-p(R1-Wo1,CPE1)"
    params = [0.1, 0.01, 1, 1000, 15, 0.9]
    frequencies = [1000.0, 5.0, 0.01]

    cg = CircuitGraph(circuit)
    assert len(cg.execution_order) == 7
    assert len(cg.compute(frequencies, *params)) == len(frequencies)
    assert cg.calculate_circuit_length() == 6

    import matplotlib.pyplot as plt

    f, ax = plt.subplots()
    cg.visualize_graph(ax=ax)
    plt.close(f)

    # Test multiple parallel elements
    circuit = "R0-p(C1,R1,R2)"

    assert len(CircuitGraph(circuit).execution_order) == 6

    # Test nested parallel groups
    circuit = "R0-p(p(R1, C1)-R2, C2)"

    assert len(CircuitGraph(circuit).execution_order) == 9

    # Test parallel elements at beginning and end
    circuit = "p(C1,R1)-p(C2,R2)"

    assert len(CircuitGraph(circuit).execution_order) == 7

    # Test single element circuit
    circuit = "R1"

    assert len(CircuitGraph(circuit).execution_order) == 1


def test_RMSE():
    a = np.array([2 + 4 * 1j, 3 + 2 * 1j])
    b = np.array([2 + 4 * 1j, 3 + 2 * 1j])

    assert rmse(a, b) == 0.0

    c = np.array([2 + 4 * 1j, 1 + 4 * 1j])
    d = np.array([4 + 2 * 1j, 3 + 2 * 1j])
    assert np.isclose(rmse(c, d), 2 * np.sqrt(2))


def test_element_extraction():
    circuit = "R0-p(RR0,C1)-p(R1,C2032478)-W1"
    extracted_elements = extract_circuit_elements(circuit)
    assert extracted_elements == ["R0", "RR0", "C1", "R1", "C2032478", "W1"]


def test_bounds():
    with pytest.raises(ValueError):
        BoundsCheck(np.array([1, 2, 8]), np.array([2, 3, 4]))

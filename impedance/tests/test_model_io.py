import numpy as np
from impedance.models.circuits import CustomCircuit
import os


def test_model_io():
    # get example data
    data = np.genfromtxt(os.path.join(".", "data",
                                      "exampleData.csv"), delimiter=',')

    frequencies = data[:, 0]
    Z = data[:, 1] + 1j * data[:, 2]

    randles = CustomCircuit(initial_guess=[None, .005, .1,
                                           .005, .1, 0.9, .001, None],
                            circuit='R0-p(R1,C1)-p(R1,CPE1)-Wo1',
                            constants={'R0': 0.01, 'Wo1_1': 200})
    randles.save('./test_io.json')
    randles2 = CustomCircuit()
    randles2.load('./test_io.json')

    assert randles == randles2

    randles.fit(frequencies, Z)
    randles.save('./test_io.json')
    randles2 = CustomCircuit()
    randles2.load('./test_io.json')

    assert str(randles) == str(randles2)
    assert randles == randles2

    fitted_template = CustomCircuit()
    fitted_template.load('test_io.json', fitted_as_initial=True)


def test_refit_after_load_fitted_as_initial():
    # Regression test for #310: loading a fitted model with
    # fitted_as_initial=True stores initial_guess as a numpy array, which
    # broke the subsequent ``fit`` call because the emptiness check compared
    # the array against ``[]`` (raising a broadcasting ValueError).
    data = np.genfromtxt(os.path.join(".", "data",
                                      "exampleData.csv"), delimiter=',')
    frequencies = data[:, 0]
    Z = data[:, 1] + 1j * data[:, 2]

    randles = CustomCircuit(initial_guess=[.01, .005, .1, .005, .1, .9,
                                           .001, 200],
                            circuit='R0-p(R1,C1)-p(R1,CPE1)-Wo1')
    randles.fit(frequencies, Z)
    randles.save('./test_io.json')

    reloaded = CustomCircuit()
    reloaded.load('./test_io.json', fitted_as_initial=True)
    assert isinstance(reloaded.initial_guess, np.ndarray)

    # Refitting must not raise; it previously failed with
    # "operands could not be broadcast together with shapes (n,) (0,)"
    reloaded.fit(frequencies, Z)
    assert reloaded.parameters_ is not None

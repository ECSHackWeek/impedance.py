import numpy as np
from impedance.model_io import model_export, model_import
from impedance.circuits import CustomCircuit


def test_model_io():
    # get example data
    data = np.genfromtxt('./data/exampleData.csv', delimiter=',')

    frequencies = data[:, 0]
    Z = data[:, 1] + 1j*data[:, 2]

    randles = CustomCircuit(initial_guess=[.01, .005, .1, .005, .1, .001, 200],
                            circuit='R0-p(R1,C1)-p(R1,C1)-W1')
    randles.fit(frequencies, Z)

    print(randles)

    model_export(randles, './test_io.json')
    randles2 = model_import('./test_io.json')
    print(randles2)

    assert randles == randles2

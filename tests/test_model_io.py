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

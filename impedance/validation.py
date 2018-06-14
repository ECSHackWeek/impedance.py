from .circuits import CustomCircuit
import numpy as np


def rmse(a, b):
    """
    A function which calculates the root mean squared
    error between two vectors.

    Notes
    ---------
    .. math::

        RMSE = \\sqrt{\\frac{1}{n}(a-b)^2}
    """

    return(np.abs(np.sqrt(np.mean(np.square(a-b)))))


def measurementModel(frequencies, impedances, algorithm='SLSQP',
                     max_k=7, R_guess=0.1, C_guess=10):
    """ Runs a measurement model test for validating impedance data

    Iteratively add RC circuit elements until the error converges.
    If error does not converge, it indicates that the data doesn't meet
    standards for linearity.

    Notes
    ---------
    .. math::

        RMSE = R_0 + \\sum_{0}^{k} R_i || C_i

    Parameters
    ---------
    frequencies: np.ndarray
        A list of frequencies to test
    impedances: np.ndarray of complex numbers
        A list of values to match to
    max_k: int
        The maximum number of RC elements to fit
    initial_guess: np.ndarray
        Initial guesses for R and C elements
    """

    circuit = "R_0"
    initial_guess = [R_guess]
    error_list = []
    model_list = []

    print('--- Running Measurement Model ---')
    for i in range(max_k):
        circuit += "-p(R_{},C_{})".format((i+1) % 9, (i+1) % 9)
        initial_guess.append(R_guess)
        initial_guess.append(C_guess)
        measModel = CustomCircuit(initial_guess=initial_guess,
                                  circuit=circuit, algorithm=algorithm)

        measModel.fit(frequencies, impedances)
        initial_guess = list(measModel.parameters_)
        model_list.append(measModel)
        fit = measModel.predict(frequencies)
        error = rmse(impedances, fit)
        error_list.append(error)

        print('Num elements: {}  Error: {:.2e}'.format(i+1, error))

    return model_list, error_list

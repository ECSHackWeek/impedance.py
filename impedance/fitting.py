from .circuit_elements import R, C, L, W, A, E, G, T, s, p  # noqa: F401
import numpy as np
from scipy.optimize import curve_fit


def rmse(a, b):
    """
    A function which calculates the root mean squared error
    between two vectors.

    Notes
    ---------
    .. math::

        RMSE = \\sqrt{\\frac{1}{n}(a-b)^2}
    """

    n = len(a)
    return np.linalg.norm(a - b) / np.sqrt(n)


def circuit_fit(frequencies, impedances, circuit, initial_guess,
                constants, method=None, bounds=None, bootstrap=False):

    """ Main function for fitting an equivalent circuit to data

    Parameters
    -----------------
    frequencies : numpy array
        Frequencies

    impedances : numpy array of dtype 'complex128'
        Impedances

    circuit : string
        string defining the equivalent circuit to be fit

    initial_guess : list of floats
        initial guesses for the fit parameters

    constants : dictionary
        parameters and their values to hold constant during fitting
        (e.g. {"RO": 0.1})

    method : {‘lm’, ‘trf’, ‘dogbox’}, optional
        Name of method to pass to scipy.optimize.curve_fit

    bounds : 2-tuple of array_like, optional
        Lower and upper bounds on parameters. Defaults to bounds on all
        parameters of 0 and np.inf, except the CPE alpha
        which has an upper bound of 1

    Returns
    ------------
    p_values : list of floats
        best fit parameters for specified equivalent circuit

    p_errors : list of floats
        one standard deviation error estimates for fit parameters

    Notes
    ---------
    Need to do a better job of handling errors in fitting.
    Currently, an error of -1 is returned.

    """

    circuit = circuit.replace('_', '')

    f = frequencies
    Z = impedances

    if bounds is None:
        lb, ub = [], []
        p_string = [x for x in circuit if x not in 'ps(),-/']
        for a, b in zip(p_string[::2], p_string[1::2]):
            for i in range(check_and_eval(a).num_params):
                if i == 0:
                    if a + b in constants.keys():
                        continue
                    else:
                        lb.append(0)
                        ub.append(np.inf)
                else:
                    if a + b + '_{}'.format(i) in constants.keys():
                        continue
                    else:
                        lb.append(0)
                        if a == "E" and i == 1:
                            ub.append(1)
                        else:
                            ub.append(np.inf)

        bounds = ((lb), (ub))

    popt, pcov = curve_fit(wrapCircuit(circuit, constants), f,
                           np.hstack([Z.real, Z.imag]), p0=initial_guess,
                           method=method, bounds=bounds, maxfev=100000,
                           ftol=1E-13)

    perror = np.sqrt(np.diag(pcov))

    return popt, perror


def wrapCircuit(circuit, constants):
    """ wraps function so we can pass the circuit string """
    def wrappedCircuit(frequencies, *parameters):
        """ returns a stacked

        Parameters
        ----------
        circuit : string
        constants : dict
        parameters : list of floats
        frequencies : list of floats

        Returns
        -------
        array of floats

        """

        x = eval(buildCircuit(circuit, frequencies, *parameters,
                              constants=constants, eval_string='',
                              index=0)[0])
        y_real = np.real(x)
        y_imag = np.imag(x)

        return np.hstack([y_real, y_imag])
    return wrappedCircuit


def buildCircuit(circuit, frequencies, *parameters,
                 constants=None, eval_string='', index=0):
    """ recursive function that transforms a circuit, parameters, and
    frequencies into a string that can be evaluated

    Parameters
    ----------
    circuit: str
    frequencies: list/tuple/array of floats
    parameters: list/tuple/array of floats
    constants: dict

    Returns
    -------
    eval_string: str
        Python expression for calculating the resulting fit
    index: int
        Tracks parameter index through recursive calling of the function
    """

    parameters = np.array(parameters).tolist()
    frequencies = np.array(frequencies).tolist()
    circuit = circuit.replace(' ', '')

    def parse_circuit(circuit, parallel=False, series=False):
        """ Splits a circuit string by either dashes (series) or commas
            (parallel) outside of any paranthesis. Removes any leading 'p('
            or trailing ')' when in parallel mode """

        assert parallel != series, \
            'Exactly one of parallel or series must be True'

        def count_parens(string):
            return string.count('('), string.count(')')

        if parallel:
            special = ','
            if circuit.endswith(')') and circuit.startswith('p('):
                circuit = circuit[2:-1]
        if series:
            special = '-'

        split = circuit.split(special)
        result = []
        skipped = []
        for i, sub_str in enumerate(split):
            if i not in skipped:
                if '(' not in sub_str and ')' not in sub_str:
                    result.append(sub_str)
                else:
                    open_parens, closed_parens = count_parens(sub_str)
                    if open_parens == closed_parens:
                        result.append(sub_str)
                    else:
                        uneven = True
                        while i < len(split) - 1 and uneven:
                            sub_str += special + split[i+1]

                            open_parens, closed_parens = count_parens(sub_str)
                            uneven = open_parens != closed_parens

                            i += 1
                            skipped.append(i)
                        result.append(sub_str)
        return result

    parallel = parse_circuit(circuit, parallel=True)
    series = parse_circuit(circuit, series=True)

    if series is not None and len(series) > 1:
        eval_string += "s(["
        split = series
    elif parallel is not None and len(parallel) > 1:
        eval_string += "p(["
        split = parallel

    for i, elem in enumerate(split):
        if ',' in elem or '-' in elem:
            eval_string, index = buildCircuit(elem, frequencies,
                                              *parameters,
                                              constants=constants,
                                              eval_string=eval_string,
                                              index=index)
        else:
            param_string = ""
            elem_number = check_and_eval(elem[0]).num_params
            param_list = []
            for j in range(elem_number):
                if elem_number > 1:
                    current_elem = elem + '_{}'.format(j)
                else:
                    current_elem = elem

                if current_elem in constants.keys():
                    param_list.append(constants[current_elem])
                else:
                    param_list.append(parameters[index])
                    index += 1

            param_string += str(param_list)
            new = elem[0] + '(' + param_string + ',' + str(frequencies) + ')'
            eval_string += new

        if i == len(split) - 1:
            eval_string += '])'
        else:
            eval_string += ','

    return eval_string, index


def calculateCircuitLength(circuit):
    elements = [R, C, L, W, A, E, G, T]
    length = 0
    for element in elements:
        num_params = element.num_params
        length += num_params*circuit.count(element.__name__)
    return length


def check_and_eval(element):
    allowed_elements = ['R', 'C', 'L', 'W', 'A', 'E', 'G', 'T']
    if element not in allowed_elements or len(element) != 1:
        raise ValueError
    else:
        return eval(element)

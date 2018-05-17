from .circuit_elements import *
from scipy.optimize import leastsq

def circuit_fit(frequencies, impedances, circuit, initial_guess):
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

    Returns
    ------------
    p_values : list of floats
        best fit parameters for specified equivalent circuit

    p_errors : list of floats
        error estimates for fit parameters

    Notes
    ---------
    Need to do a better job of handling errors in fitting.
    Currently, an error of -1 is returned.

    """

    circuit = circuit.replace('_', '')
    
    f = frequencies
    Z = impedances
    
    # takes out the _s
#    print(circuit)
#    print(f)
#    print(Z)

    p_values, covar, _, _, ier = leastsq(residuals, initial_guess,
                                         args=(Z, f, circuit),
                                         maxfev=100000, ftol=1E-13,
                                         full_output=True)

    p_error = []
    if ier in [1, 2, 3, 4] and covar is not None:
        s_sq = (residuals(p_values, Z, frequencies, circuit)**2).sum()
        p_cov = covar * s_sq/(len(Z) - len(p_values))
        for i, __ in enumerate(covar):
            p_error.append(np.absolute(p_cov[i][i])**0.5)
    else:
        p_error = len(p_values)*[-1]

    return p_values, p_error


def residuals(param, Z, f, circuit):
    """ Calculates the residuals between a given circuit/parameters
    (fit) and `Z`/`f` (data). Minimized by scipy.leastsq()

    Parameters
    ----------
    param : array of floats
        parameters for evaluating the circuit

    Z : array of complex numbers
        impedance data being fit

    f : array of floats
        frequencies to evaluate

    circuit : str
        string defining the circuit

    Returns
    -------
    residual : ndarray
        returns array of size 2*len(f) with both real and imaginary residuals
    """
    err = Z - computeCircuit(circuit, param.tolist(), f.tolist())
    z1d = np.zeros(Z.size*2, dtype=np.float64)
    z1d[0:z1d.size:2] = err.real
    z1d[1:z1d.size:2] = err.imag
    if valid(circuit, param):
        return z1d
    else:
        return 1e6*np.ones(Z.size*2, dtype=np.float64)


def valid(circuit, param):
    """ checks validity of parameters

    Parameters
    ----------
    circuit : string
        string defining the circuit

    param : list
        list of parameter values

    Returns
    -------
    valid : boolean

    Notes
    -----
    All parameters are considered valid if they are greater than zero --
    except for E2 (the exponent of CPE) which also must be less than one.

    """

    p_string = [p for p in circuit if p not in 'ps(),-/']

    for i, (a, b) in enumerate(zip(p_string[::2], p_string[1::2])):
        if str(a+b) == "E2":
            if param[i] <= 0 or param[i] >= 1:
                return False
        else:
            if param[i] <= 0:
                return False

    return True


def computeCircuit(circuit, parameters, frequencies):
    """ evaluates a circuit string for a given set of parameters and frequencies

    Parameters
    ----------
    circuit : string
    parameters : list of floats
    frequencies : list of floats

    Returns
    -------
    array of floats
    """
#    print(buildCircuit(circuit, parameters, frequencies))
    return eval(buildCircuit(circuit, parameters, frequencies))


def buildCircuit(circuit, parameters, frequencies):
    """ transforms a circuit, parameters, and frequencies into a string
    that can be evaluated

    Parameters
    ----------
    circuit : str
    parameters : list of floats
    frequencies : list of floats

    Returns
    -------
    eval_string : str
        Python expression for calculating the resulting fit
    """

    series_string = "s(["
    for elem in circuit.split("-"):
        element_string = ""
        if "p" in elem:
            parallel_string = "p(("
            for par in elem.strip("p()").split(","):
                param_string = ""
                elem_type = par[0]
                elem_number = len(par.split("/"))

                param_string += str(parameters[0:elem_number])
                parameters = parameters[elem_number:]

                new_elem = (elem_type + "(" + param_string + "," +
                                        str(frequencies) + "),")
                parallel_string += new_elem

            element_string = parallel_string.strip(",") + "))"
        else:
            param_string = ""
            elem_type = elem[0]
            elem_number = len(elem.split("/"))

            param_string += str(parameters[0:elem_number])
            parameters = parameters[elem_number:]

            element_string = (elem_type + "(" + param_string + "," +
                                          str(frequencies) + ")")

        series_string += element_string + ","

    eval_string = series_string.strip(",") + "])"

    return eval_string

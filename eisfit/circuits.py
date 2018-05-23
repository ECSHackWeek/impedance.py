from .fitting import circuit_fit, computeCircuit, calculateCircuitLength
import numpy as np


class BaseCircuit:
    """ Base class for equivalent circuit models """
    def __init__(self, initial_guess=None, name=None,
                 algorithm='leastsq', bounds=None):
        """ Base constructor for any equivalent circuit model """

        # if supplied, check that initial_guess is valid and store
        if initial_guess is not None:
            for i in initial_guess:
                assert isinstance(i, (float, int, np.int32, np.float64)),\
                    'value {} in initial_guess is not a number'.format(i)

        # initalize class attributes
        self.initial_guess = initial_guess
        self.name = name
        self.algorithm = algorithm
        self.bounds = bounds

        # initialize fit parameters and confidence intervals
        self.parameters_ = None
        self.conf_ = None

    def fit(self, frequencies, impedance):
        """ Fit the circuit model

        Parameters
        ----------
        frequencies: numpy array
            Frequencies

        impedance: numpy array of dtype 'complex128'
            Impedance values to fit

        Returns
        -------
        self: returns an instance of self

        """

        # check that inputs are valid:
        #    frequencies: array of numbers
        #    impedance: array of complex numbers
        #    impedance and frequency match in length

        assert isinstance(frequencies, np.ndarray),\
            'frequencies is not of type np.ndarray'
        assert isinstance(frequencies[0], (float, int, np.int32, np.float64)),\
            'frequencies does not contain a number'
        assert isinstance(impedance, np.ndarray),\
            'impedance is not of type np.ndarray'
        assert isinstance(impedance[0], (complex, np.complex128)),\
            'impedance does not contain complex numbers'
        assert len(frequencies) == len(impedance),\
            'mismatch in length of input frequencies and impedances'

        if self.initial_guess is not None:
            self.parameters_, _ = circuit_fit(frequencies, impedance,
                                              self.circuit, self.initial_guess,
                                              self.algorithm,
                                              bounds=self.bounds)
        else:
            # TODO auto calc guess
            raise ValueError('no initial guess supplied')

        return self

    def _is_fit(self):
        """ check if model has been fit (parameters_ is not None) """
        if self.parameters_ is not None:
            return True
        else:
            return False

    def predict(self, frequencies):
        """ Predict impedance using a fit equivalent circuit model

        Parameters
        ----------
        frequencies: numpy array
            Frequencies

        Returns
        -------
        impedance: numpy array of dtype 'complex128'
            Predicted impedance

        """

        # check that inputs are valid:
        #    frequencies: array of numbers

        assert isinstance(frequencies, np.ndarray),\
            'frequencies is not of type np.ndarray'
        assert isinstance(frequencies[0], (float, int, np.int32, np.float64)),\
            'frequencies does not contain a number'

        if self._is_fit():
            return computeCircuit(self.circuit,
                                  self.parameters_.tolist(),
                                  frequencies.tolist())

        else:
            raise ValueError("The model hasn't been fit yet. " +
                             "Please call the `.fit` method before trying to" +
                             " predict model output")

    def __str__(self):
        """ Defines the pretty printing of the circuit """

        # parse the element names from the circuit string
        names = self.circuit.replace('p', '').replace('(', '').replace(')', '')
        names = names.replace(',', '-').replace('/', '-').split('-')

        to_print  = '\n-------------------------------\n'  # noqa E222
        to_print += 'Circuit: {}\n'.format(self.name)
        to_print += 'Circuit string: {}\n'.format(self.circuit)
        to_print += 'Algorithm: {}\n'.format(self.algorithm)

        if self._is_fit():
            to_print += 'Fit: True\n'
            to_print += 'Fit parameters:\n'
            for name, param in zip(names, self.parameters_):
                to_print += '\t{} = {:.2e}\n'.format(name, param)
        else:
            to_print += 'Fit: False\n'
            to_print += 'Initial guesses:\n'
            for name, param in zip(names, self.initial_guess):
                to_print += '\t{} = {:.2e}\n'.format(name, param)

        to_print += '\n-------------------------------\n'
        return to_print


class Randles(BaseCircuit):
    def __init__(self, CPE=False, **kwargs):
        """ Constructor for the Randles' circuit class

        Parameters
        ----------
        CPE: boolean
            Use a constant phase element instead of a capacitor
        """
        super().__init__(**kwargs)

        if CPE:
            self.name = 'Randles w/ CPE'
            self.circuit = 'R_0-p(R_1,E_1/E_2)-W_1/W_2'
            circuit_length = calculateCircuitLength(self.circuit)
            assert len(self.initial_guess) == circuit_length, \
                'Initial guess length needs to be equal to parameter length'
        else:
            self.name = 'Randles'
            self.circuit = 'R_0-p(R_1,C_1)-W_1/W_2'
            circuit_length = calculateCircuitLength(self.circuit)
            assert len(self.initial_guess) == circuit_length, \
                'Initial guess length needs to be equal to parameter length'


class DefineCircuit(BaseCircuit):
    def __init__(self, circuit=None, **kwargs):
        """ Constructor for a customizable equivalent circuit model

        Parameters
        ----------
        circuit: string
            A string that should be interpreted as an equivalent circuit

        """

        super().__init__(**kwargs)
        self.circuit = circuit

        circuit_length = calculateCircuitLength(self.circuit)
        assert len(self.initial_guess) == circuit_length, \
            'Initial guess length needs to be equal to {circuit_length}'


class FlexiCircuit(BaseCircuit):
    def __init__(self, max_elements=None, generations=2,
                 popsize=30, initial_guess=None):
        """ Constructor for the Flexible Circuit class

        Parameters
        ----------
        max_elements: integer
            The maximum number of elements available to the algorithm
        solve_time: integer
            The maximum allowed solve time, in seconds.

        """

        self.name = 'Flexible Circuit'
        self.initial_guess = initial_guess
        self.generations = generations
        self.popsize = popsize
        self.max_elements = max_elements
#        self.bounds = bounds

    def fit(self, frequencies, impedances):
        from scipy.optimize import leastsq
        from .genetic import make_population
        from .fitting import residuals
        n = 5
        f = frequencies
        Z = impedances
        for i in range(self.generations):
            scores = []
            self.population = make_population(self.popsize, n)
            for pop in self.population:
                self.circuit = pop
                print(self.circuit)
                circuit_length = calculateCircuitLength(self.circuit)
#                for j in range(n-4,n+4):
#                    print(residuals(self.initial_guess,Z,f,self.circuit))
#                    try:
#                        print(self.circuit)
                self.initial_guess = list(np.ones(circuit_length)/10)
#                        print(residuals(self.initial_guess,Z,F,))
#                        print(self.initial_guess)
                p_values, covar, ff, _, _ = leastsq(residuals,
                                                    self.initial_guess,
                                                    args=(Z, f, self.circuit),
                                                    maxfev=100000, ftol=1E-13,
                                                    full_output=True)

                print(p_values)
                scores.append([np.square(ff['fvec']).mean(), pop])

        print(scores)
        return scores

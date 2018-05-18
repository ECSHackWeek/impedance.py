from .fitting import circuit_fit, computeCircuit
import numpy as np

class BaseCircuit:
    """ A base class for all circuits

    """
    def __init__(self, initial_guess=None):
        """
        Constructor for the Randles' circuit class


        """
        if initial_guess is not None:
            for i in initial_guess:
                assert type(i) == type(0.5) or type(i) == type(1) or \
                type(i) == type(np.array([1])[0]) or type(i) == type(np.array([1.5])[0]), \
                ('value {} in initial_guess is not a number'.format(i))
        self.initial_guess = initial_guess
        self.parameters_ = None

    def fit(self, frequencies, impedance):
        """
        Fit the circuit model

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
        # tests
        import numpy as np
        assert type(frequencies) == type([1.5]) or type(frequencies) == type(np.array([1.5]))
        assert len(frequencies) == len(impedance)
        for i in frequencies:
            assert type(i) == type(0.5) or type(i) == type(1) or \
            type(i) == type(np.array([1])[0]) or type(i) == type(np.array([1.5])[0]), \
            ('value {} in initial_guess is not a number'.format(i))
        # check_valid_impedance()
        if self.initial_guess is not None:
            self.parameters_, _ = circuit_fit(frequencies, impedance, self.circuit, self.initial_guess)
        else:
            # TODO auto calc guess
            raise ValueError('no initial guess supplied')

        return self

    def _is_fit(self):
        if self.parameters_ is not None:
            return True
        else:
            return False

    def predict(self, frequencies):
        """ Predict impedance using a fit model

        Parameters
        ----------
        frequencies: numpy array
            Frequencies

        Returns
        -------
        impedance: numpy array of dtype 'complex128'
            Predicted impedance

        """

        if self._is_fit():
            # print('Output! {}'.format(self.parameters_))

            return computeCircuit(self.circuit,
                                   self.parameters_.tolist(),
                                   frequencies.tolist())

        else:
            raise ValueError("The model hasn't been fit yet")

    def __repr__(self):
        """
        Defines the pretty printing of the circuit

        """
        if self._is_fit():
            return "{} circuit (fit values={}, circuit={})".format(self.name, self.parameters_, self.circuit)
        else:
            return "{} circuit (initial_guess={}, circuit={})".format(self.name, self.initial_guess, self.circuit)

class Randles(BaseCircuit):
    def __init__(self, initial_guess=None, CPE=False):
        """
        Constructor for the Randles' circuit class

        Inputs
        ------
        initial_guess: A list of values to use as the initial guess for element values
        CPE: Whether or not to use constant phase elements in place of a Warburg element

        Methods
        -------

        .fit(frequencies, impedances)
            frequencies: A list of frequencies where the values should be tested
            impedances: A list of impedances used to fitting using scipy's least_squares fitting algorithm.
        .predict(frequencies)
            frequencies: A list of frequencies where new values will be calculated



        """
        self.name = 'Randles'
        # write some asserts to enforce typing
        if initial_guess is not None:
            for i in initial_guess:
                assert type(i) == type(0.5) or type(i) == type(1) or \
                type(i) == type(np.array([1])[0]) or type(i) == type(np.array([1.5])[0]), \
                ('value {} in initial_guess is not a number'.format(i))

        if CPE:
            self.circuit = 'R_0-p(R_1,E_1/E_2)-W_1/W_2'
            circuit_length = 6
            assert len(initial_guess) == circuit_length, 'Initial guess length needs to be equal to {circuit_length}'
        else:
            self.circuit = 'R_0-p(R_1,C_1)-W_1/W_2'

            circuit_length = 5
            assert len(initial_guess) == circuit_length, 'Initial guess length needs to be equal to {circuit_length}'


        self.initial_guess = initial_guess
        self.parameters_ = None

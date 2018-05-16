from .fitting import circuit_fit, computeCircuit

class Randles:
    def __init__(self, initial_guess=None, CPE=False):
        """
        Constructor for the Randles' circuit class


        """

        if CPE:
            self.circuit = 'R_0-p(R_1,E_1/E_2)-W_1/W_2'
        else:
            self.circuit = 'R_0-p(R_1,C_1)-W_1/W_2'

        self.initial_guess = initial_guess
        self.parameters_ = None

    def __repr__(self):
        """
        Defines the pretty printing of the circuit

        """
        return "Randles circuit (initial_guess={}, circuit={})".format(self.initial_guess, self.circuit)

    def fit(self, frequencies, impedance):
        """
        Fit the Randles circuit model

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
        """ Predict using the fit Randles model

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

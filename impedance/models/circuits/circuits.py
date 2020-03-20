from .fitting import circuit_fit, buildCircuit
from .fitting import calculateCircuitLength, check_and_eval
from impedance.visualization import plot_altair, plot_bode, plot_nyquist
from .elements import circuit_elements, get_element_from_name

import json
import matplotlib.pyplot as plt
import numpy as np


class BaseCircuit:
    """ Base class for equivalent circuit models """
    def __init__(self, initial_guess=[], constants=None, name=None):
        """ Base constructor for any equivalent circuit model

        Parameters
        ----------
        initial_guess: numpy array
            Initial guess of the circuit values

        constants : dict
            (Optional) Parameters and values to hold constant during fitting
            (e.g. {"R0": 0.1})

        name : str
            (Optional) Name for the circuit
        """

        # if supplied, check that initial_guess is valid and store
        initial_guess = list(filter(None, initial_guess))
        for i in initial_guess:
            assert isinstance(i, (float, int, np.int32, np.float64)),\
                'value {} in initial_guess is not a number'.format(i)

        # initalize class attributes
        self.initial_guess = initial_guess
        if constants is not None:
            self.constants = constants
        else:
            self.constants = {}
        self.name = name

        # initialize fit parameters and confidence intervals
        self.parameters_ = None
        self.conf_ = None

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            matches = []
            for key, value in self.__dict__.items():
                if isinstance(value, np.ndarray):
                    matches.append((value == other.__dict__[key]).all())
                else:
                    matches.append(value == other.__dict__[key])
            return np.array(matches).all()
        else:
            raise TypeError('Comparing object is not of the same type.')

    def fit(self, frequencies, impedance, method=None, bounds=None):
        """ Fit the circuit model

        Parameters
        ----------
        frequencies: numpy array
            Frequencies

        impedance: numpy array of dtype 'complex128'
            Impedance values to fit

        method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Name of method to pass to scipy.optimize.curve_fit

        bounds: 2-tuple of array_like, optional
            Lower and upper bounds on parameters. Defaults to bounds on all
            parameters of 0 and np.inf, except the CPE alpha
            which has an upper bound of 1

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
            parameters, conf = circuit_fit(frequencies, impedance,
                                           self.circuit, self.initial_guess,
                                           self.constants, method=method,
                                           bounds=bounds)
            self.parameters_ = parameters
            if conf is not None:
                self.conf_ = conf
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

    def predict(self, frequencies, use_initial=False):
        """ Predict impedance using a fit equivalent circuit model

        Parameters
        ----------
        frequencies: numpy array
            Frequencies

        use_initial: boolean
            If true and a fit was already completed,
            use the initial parameters instead

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

        if self._is_fit() and not use_initial:
            return eval(buildCircuit(self.circuit, frequencies,
                                     *self.parameters_,
                                     constants=self.constants, eval_string='',
                                     index=0)[0],
                        circuit_elements)
        else:
            print("Simulating circuit based on initial parameters")
            return eval(buildCircuit(self.circuit, frequencies,
                                     *self.initial_guess,
                                     constants=self.constants, eval_string='',
                                     index=0)[0],
                        circuit_elements)

    def get_param_names(self):
        """ Converts circuit string to names and units """

        # parse the element names from the circuit string
        names = self.circuit.replace('p', '').replace('(', '').replace(')', '')
        names = names.replace(',', '-').replace(' ', '').split('-')

        full_names, all_units = [], []
        for name in names:
            elem = get_element_from_name(name)
            num_params = check_and_eval(elem).num_params
            units = check_and_eval(elem).units
            if num_params > 1:
                for j in range(num_params):
                    full_name = '{}_{}'.format(name, j)
                    if full_name not in self.constants.keys():
                        full_names.append(full_name)
                        all_units.append(units[j])
            else:
                if name not in self.constants.keys():
                    full_names.append(name)
                    all_units.append(units[0])

        return full_names, all_units

    def __str__(self):
        """ Defines the pretty printing of the circuit"""

        to_print = '\n'
        if self.name is not None:
            to_print += 'Name: {}\n'.format(self.name)
        to_print += 'Circuit string: {}\n'.format(self.circuit)
        to_print += "Fit: {}\n".format(self._is_fit())

        if len(self.constants) > 0:
            to_print += '\nConstants:\n'
            for name, value in self.constants.items():
                elem = get_element_from_name(name)
                units = check_and_eval(elem).units
                if '_' in name:
                    unit = units[int(name.split('_')[-1])]
                else:
                    unit = units[0]
                to_print += '  {:>5} = {:.2e} [{}]\n'.format(name, value, unit)

        names, units = self.get_param_names()
        to_print += '\nInitial guesses:\n'
        for name, unit, param in zip(names, units, self.initial_guess):
            to_print += '  {:>5} = {:.2e} [{}]\n'.format(name, param, unit)
        if self._is_fit():
            params, confs = self.parameters_, self.conf_
            to_print += '\nFit parameters:\n'
            for name, unit, param, conf in zip(names, units, params, confs):
                to_print += '  {:>5} = {:.2e}'.format(name, param)
                to_print += '  (+/- {:.2e}) [{}]\n'.format(conf, unit)

        return to_print

    def plot(self, ax=None, f_data=None, Z_data=None, kind='altair', **kwargs):
        """ visualizes the model and optional data as a nyquist,
            bode, or altair (interactive) plots

        Parameters
        ----------
        ax: matplotlib.axes
            axes to plot on
        f_data: np.array of type float
            Frequencies of input data (for Bode plots)
        Z_data: np.array of type complex
            Impedance data to plot
        kind: {'altair', 'nyquist', 'bode'}
            type of plot to visualize

        Other Parameters
        ----------------
        **kwargs : optional
            If kind is 'nyquist' or 'bode', used to specify additional
             `matplotlib.pyplot.Line2D` properties like linewidth,
             line color, marker color, and labels.
            If kind is 'altair', used to specify nyquist height as `size`

        Returns
        -------
        ax: matplotlib.axes
            axes of the created nyquist plot
        """

        if kind == 'nyquist':
            if ax is None:
                fig, ax = plt.subplots(figsize=(5, 5))

            if Z_data is not None:
                ax = plot_nyquist(ax, Z_data, ls='', marker='s', **kwargs)

            if self._is_fit():
                if f_data is not None:
                    f_pred = f_data
                else:
                    f_pred = np.logspace(5, -3)

                Z_fit = self.predict(f_pred)
                ax = plot_nyquist(ax, Z_fit, ls='-', marker='', **kwargs)
            return ax
        elif kind == 'bode':
            if ax is None:
                fig, ax = plt.subplots(nrows=2, figsize=(5, 5))

            if Z_data is not None:
                ax = plot_bode(ax, f_data, Z_data, ls='', marker='s', **kwargs)

            if self._is_fit():
                if f_data is not None:
                    f_pred = f_data
                else:
                    f_pred = np.logspace(5, -3)

                Z_fit = self.predict(f_pred)
                ax = plot_bode(ax, f_pred, Z_fit, ls='-', marker='', **kwargs)
            return ax
        elif kind == 'altair':
            plot_dict = {}

            if Z_data is not None and f_data is not None:
                plot_dict['data'] = {'f': f_data, 'Z': Z_data}

            if self._is_fit():
                if f_data is not None:
                    f_pred = f_data
                else:
                    f_pred = np.logspace(5, -3)

                Z_fit = self.predict(f_pred)
                if self.name is not None:
                    name = self.name
                else:
                    name = 'fit'
                plot_dict[name] = {'f': f_pred, 'Z': Z_fit, 'fmt': '-'}

            chart = plot_altair(plot_dict, **kwargs)
            return chart
        else:
            raise ValueError("Kind must be one of 'altair'," +
                             f"'nyquist', or 'bode' (received {kind})")

    def save(self, filepath):
        """ Exports a model to JSON

        Parameters
        ----------
        filepath: str
            Destination for exporting model object
        """

        model_string = self.circuit
        model_name = self.name

        initial_guess = self.initial_guess

        if self._is_fit():
            parameters_ = list(self.parameters_)
            model_conf_ = list(self.conf_)

            data_dict = {"Name": model_name,
                         "Circuit String": model_string,
                         "Initial Guess": initial_guess,
                         "Constants": self.constants,
                         "Fit": True,
                         "Parameters": parameters_,
                         "Confidence": model_conf_,
                         }
        else:
            data_dict = {"Name": model_name,
                         "Circuit String": model_string,
                         "Initial Guess": initial_guess,
                         "Constants": self.constants,
                         "Fit": False}

        with open(filepath, 'w') as f:
            json.dump(data_dict, f)

    def load(self, filepath, fitted_as_initial=False):
        """ Imports a model from JSON

        Parameters
        ----------
        filepath: str
            filepath to JSON file to load model from

        fitted_as_initial: bool
            If true, loads the model's fitted parameters
            as initial guesses

            Otherwise, loads the model's initial and
            fitted parameters as a completed model
        """

        json_data_file = open(filepath, 'r')
        json_data = json.load(json_data_file)

        model_name = json_data["Name"]
        if model_name == 'None':
            model_name = None

        model_string = json_data["Circuit String"]
        model_initial_guess = json_data["Initial Guess"]
        model_constants = json_data["Constants"]

        self.initial_guess = model_initial_guess
        self.circuit = model_string
        print(self.circuit)
        self.constants = model_constants
        self.name = model_name

        if json_data["Fit"]:
            if fitted_as_initial:
                self.initial_guess = np.array(json_data['Parameters'])
            else:
                self.parameters_ = np.array(json_data["Parameters"])
                self.conf_ = np.array(json_data["Confidence"])


class Randles(BaseCircuit):
    """ A Randles circuit model class """
    def __init__(self, CPE=False, **kwargs):
        """ Constructor for the Randles' circuit class

        Parameters
        ----------
        initial_guess: numpy array
            Initial guess of the circuit values

        CPE: boolean
            Use a constant phase element instead of a capacitor
        """
        super().__init__(**kwargs)

        if CPE:
            self.name = 'Randles w/ CPE'
            self.circuit = 'R0-p(R1,CPE1)-Wo1'
        else:
            self.name = 'Randles'
            self.circuit = 'R0-p(R1,C1)-Wo1'

        circuit_len = calculateCircuitLength(self.circuit)

        assert len(self.initial_guess) + len(self.constants) == circuit_len, \
            'The number of initial guesses + ' + \
            'the number of constants ({})'.format(len(self.initial_guess)) + \
            ' needs to be equal to ' + \
            'the circuit length ({})'.format(circuit_len)


class CustomCircuit(BaseCircuit):
    def __init__(self, circuit='', **kwargs):
        """ Constructor for a customizable equivalent circuit model

        Parameters
        ----------
        initial_guess: numpy array
            Initial guess of the circuit values

        circuit: string
            A string that should be interpreted as an equivalent circuit


        Notes
        -----
        A custom circuit is defined as a string comprised of elements in series
        (separated by a `-`) and elements in parallel (grouped as (x,y)).
        Elements with two or more parameters are separated by a forward slash
        (`/`).

        Example:
            Randles circuit is given by 'R0-p(R1,C1)-W1/W2'

        """

        super().__init__(**kwargs)
        self.circuit = circuit

        circuit_len = calculateCircuitLength(self.circuit)

        assert len(self.initial_guess) + len(self.constants) == circuit_len, \
            'The number of initial guesses + ' + \
            'the number of constants ({})'.format(len(self.initial_guess)) + \
            ' needs to be equal to ' + \
            'the circuit length ({})'.format(circuit_len)

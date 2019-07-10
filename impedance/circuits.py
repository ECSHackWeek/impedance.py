from .fitting import circuit_fit, buildCircuit
from .fitting import calculateCircuitLength, check_and_eval
from .plotting import plot_nyquist
from .circuit_elements import R, C, L, W, A, E, G, T, s, p  # noqa: F401

import numpy as np
import os

import matplotlib as mpl
if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt  # noqa E402


class BaseCircuit:
    """ Base class for equivalent circuit models """
    def __init__(self, initial_guess, name=None, bounds=None):
        """ Base constructor for any equivalent circuit model

        Parameters
        ----------
        initial_guess: numpy array
            Initial guess of the circuit values
        """

        # if supplied, check that initial_guess is valid and store
        for i in initial_guess:
            assert isinstance(i, (float, int, np.int32, np.float64)),\
                'value {} in initial_guess is not a number'.format(i)

        # initalize class attributes
        self.initial_guess = initial_guess
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

    def fit(self, frequencies, impedance, method='lm', bounds=None):
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
                                           method=method, bounds=bounds)
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
                                     *self.parameters_, eval_string='',
                                     index=0)[0])
        else:
            print("Simulating circuit based on initial parameters")
            return eval(buildCircuit(self.circuit, frequencies,
                                     *self.initial_guess, eval_string='',
                                     index=0)[0])

    def get_param_names(self):
        """Converts circuit string to names"""

        # parse the element names from the circuit string
        names = self.circuit.replace('p', '').replace('(', '').replace(')', '')
        names = names.replace(',', '-').replace(' ', '').split('-')

        full_names = []
        for name in names:
            num_params = check_and_eval(name[0]).num_params
            if num_params > 1:
                for j in range(num_params):
                    full_names.append('{}_{}'.format(name, j))
            else:
                full_names.append(name)

        return full_names

    def get_verbose_string(self):

        """ Defines the pretty printing of all data in the circuit"""
        names = self.get_param_names()

        to_print  = '\n-------------------------------\n'  # noqa E222
        to_print += 'Circuit: {}\n'.format(self.name)
        to_print += 'Circuit string: {}\n'.format(self.circuit)

        if self._is_fit():
            to_print += "Fit: True\n"
        else:
            to_print += "Fit: False\n"

        to_print += '\n-------------------------------\n'
        to_print += 'Initial guesses:\n'
        for name, param in zip(names, self.initial_guess):
            to_print += '\t{} = {:.2e}\n'.format(name, param)
        if self._is_fit():
            to_print += '\n-------------------------------\n'
            to_print += 'Fit parameters:\n'
            for name, param, conf in zip(names, self.parameters_, self.conf_):
                to_print += '\t{} = {:.2e}'.format(name, param)
                to_print += '\t(+/- {:.2e})\n'.format(conf)

        return to_print

    def __str__(self):
        """ Defines the pretty printing of the circuit """

        names = self.get_param_names()

        to_print  = '\n-------------------------------\n'  # noqa E222
        to_print += 'Circuit: {}\n'.format(self.name)
        to_print += 'Circuit string: {}\n'.format(self.circuit)

        if self._is_fit():
            to_print += "Fit: True\n"
        else:
            to_print += "Fit: False\n"

        if self._is_fit():
            to_print += '\n-------------------------------\n'
            to_print += 'Fit parameters:\n'
            for values in zip(names, self.parameters_, self.conf_):
                to_print += '\t{} = {:.2e} +/- {:.2e}\n'.format(*values)
        else:
            to_print += '\n-------------------------------\n'
            to_print += 'Initial guesses:\n'
            for name, param in zip(names, self.initial_guess):
                to_print += '\t{} = {:.2e}\n'.format(name, param)

        return to_print

    def plot(self, ax=None, f_data=None, Z_data=None,
             conf_bounds=None, scale=1, units='Ohms'):
        """ a convenience method for plotting Nyquist plots


        Parameters
        ----------
        f_data: np.array of type float
            Frequencies of input data (for Bode plots)
        Z_data: np.array of type complex
            Impedance data to plot
        conf_bounds: {'error_bars', 'filled', 'filledx', 'filledy'}, optional
            Include bootstrapped confidence bands (95%) on the predicted best
            fit model shown as either error bars or a filled confidence area.
            Confidence bands are estimated by simulating the spectra for 10000
            randomly sampled parameter sets where each of the parameters is
            sampled from a normal distribution

        Returns
        -------
        ax: matplotlib.axes
            axes of the created nyquist plot
        """

        if ax is None:
            fig, ax = plt.subplots(figsize=(5, 5))

        if Z_data is not None:
            ax = plot_nyquist(ax, f_data, Z_data,
                              scale=scale, units=units, fmt='s')

        if self._is_fit():

            if f_data is not None:
                f_pred = f_data
            else:
                f_pred = np.logspace(5, -3)

            Z_fit = self.predict(f_pred)
            ax = plot_nyquist(ax, f_data, Z_fit,
                              scale=scale, units=units, fmt='s')

            base_ylim, base_xlim = ax.get_ylim(), ax.get_xlim()

            if conf_bounds is not None:
                N = 10000
                n = len(self.parameters_)
                f_pred = np.logspace(np.log10(min(f_data)),
                                     np.log10(max(f_data)),
                                     num=100)

                params = self.parameters_
                confs = self.conf_

                full_range = np.ndarray(shape=(N, len(f_pred)), dtype=complex)
                for i in range(N):
                    self.parameters_ = params + \
                                        confs*np.random.randn(n)

                    full_range[i, :] = self.predict(f_pred)

                self.parameters_ = params

                min_Zr, min_Zi = [], []
                max_Zr, max_Zi = [], []
                xerr, yerr = [], []
                for i, Z in enumerate(Z_fit):
                    Zr, Zi = np.real(Z), np.imag(Z)
                    yr, yi = [], []
                    for run in full_range:
                        yi.append(run[i].imag)
                        yr.append(run[i].real)

                    min_Zr.append(1j*Zi + (Zr - 2*np.std(yr)))
                    max_Zr.append(1j*Zi + (Zr + 2*np.std(yr)))

                    min_Zi.append(Zr + 1j*(Zi - 2*np.std(yi)))
                    max_Zi.append(Zr + 1j*(Zi + 2*np.std(yi)))

                    xerr.append(2*np.std(yr))
                    yerr.append(2*np.std(yi))

                conf_x, conf_y = False, False
                if conf_bounds == 'error_bars':
                    ax.errorbar(Z_fit.real, -Z_fit.imag, xerr=xerr, yerr=yerr,
                                fmt='', color='#7f7f7f', zorder=-2)
                elif conf_bounds == 'filled':
                    conf_x = True
                    conf_y = True
                elif conf_bounds == 'filledx':
                    conf_x = True
                elif conf_bounds == 'filledy':
                    conf_y = True

                if conf_x:
                    ax.fill_betweenx(-np.imag(min_Zr), np.real(min_Zr),
                                     np.real(max_Zr), alpha='.2',
                                     color='#7f7f7f', zorder=-2)
                if conf_y:
                    ax.fill_between(np.real(min_Zi), -np.imag(min_Zi),
                                    -np.imag(max_Zi), alpha='.2',
                                    color='#7f7f7f', zorder=-2)

                ax.set_ylim(base_ylim)
                ax.set_xlim(base_xlim)
        return ax


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
            self.circuit = 'R0-p(R1,E1)-W1'
            circuit_length = calculateCircuitLength(self.circuit)
            assert len(self.initial_guess) == circuit_length, \
                'Initial guess length needs to be equal to parameter length'
        else:
            self.name = 'Randles'
            self.circuit = 'R0-p(R1,C1)-W1'
            circuit_length = calculateCircuitLength(self.circuit)
            assert len(self.initial_guess) == circuit_length, \
                'Initial guess length needs to be equal to parameter length'


class CustomCircuit(BaseCircuit):
    def __init__(self, circuit, **kwargs):
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

        circuit_length = calculateCircuitLength(self.circuit)
        assert len(self.initial_guess) == circuit_length, \
            'Initial guess length needs to be equal to {circuit_length}'

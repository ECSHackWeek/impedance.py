import numpy as np
from matplotlib.ticker import ScalarFormatter


class FixedOrderFormatter(ScalarFormatter):
    """Formats axis ticks using scientific notation with a constant order of
    magnitude"""
    def __init__(self, order_of_mag=0, useOffset=True, useMathText=True):
        self._order_of_mag = order_of_mag
        ScalarFormatter.__init__(self, useOffset=useOffset,
                                 useMathText=useMathText)

    def _set_orderOfMagnitude(self, range):
        """Over-riding this to avoid having orderOfMagnitude reset elsewhere"""
        self.orderOfMagnitude = self._order_of_mag


def plot_nyquist(ax, freq, Z, scale=1, units='Ohms', fmt='.-'):
    """ Convenience function for plotting nyquist plots


        Parameters
        ----------
        ax: matplotlib.axes.Axes
            axes on which to plot the nyquist plot
        freq: np.array of floats
            frequencies
        Z: np.array of complex numbers
            impedance data
        scale: float
            the scale for the axes
        units: string
            units for :math:`Z(\\omega)`
        fmt: string
            format string passed to matplotlib (e.g. '.-' or 'o')

        Returns
        -------
        ax: matplotlib.axes.Axes
    """

    ax.plot(np.real(Z), -np.imag(Z), fmt, lw=3)

    # Make the axes square
    ax.set_aspect('equal')

    # Set the labels to -imaginary vs real
    ax.set_xlabel(r'$Z^{\prime}(\omega)$ ' +
                  '$[{}]$'.format(units), fontsize=20)
    ax.set_ylabel(r'$-Z^{\prime\prime}(\omega)$ ' +
                  '$[{}]$'.format(units), fontsize=20)

    # Make the tick labels larger
    ax.tick_params(axis='both', which='major', labelsize=14)

    # Change the number of labels on each axis to five
    ax.locator_params(axis='x', nbins=5, tight=True)
    ax.locator_params(axis='y', nbins=5, tight=True)

    # Add a light grid
    ax.grid(b=True, which='major', axis='both', alpha=.5)

    # Change axis units to 10**log10(scale) and resize the offset text
    ax.xaxis.set_major_formatter(FixedOrderFormatter(-np.log10(scale)))
    ax.yaxis.set_major_formatter(FixedOrderFormatter(-np.log10(scale)))
    y_offset = ax.yaxis.get_offset_text()
    y_offset.set_size(18)
    t = ax.xaxis.get_offset_text()
    t.set_size(18)

    return ax

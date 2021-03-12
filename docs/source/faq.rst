Frequently Asked Questions
==========================

What method does impedance.py use for fitting equivalent circuit models?
------------------------------------------------------------------------
By default, fitting is performed by non-linear least squares regression of
the circuit model to impedance data via
`curve_fit <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html>`_
from the `scipy.optimize` package.[1]
Real and imaginary components are fit simultaneously with uniform
weighting, i.e. the objective function to minimize is,

.. math::
    \chi^2 = \sum_{n=0}^{N} [Z^\prime_{data}(\omega_n) - Z^\prime_{model}(\omega_n)]^2 +
                   [Z^{\prime\prime}_{data}(\omega_n) - Z^{\prime\prime}_{model}(\omega_n)]^2

where N is the number of frequencies and :math:`Z^\prime` and
:math:`Z^{\prime\prime}` are the real and imaginary components of
the impedance, respectively.
The default optimization method is the
Levenberg-Marquardt algorithm (:code:`method='lm'`) for unconstrained
problems and the Trust Region Reflective algorithm
(:code:`method='trf'`) if bounds are provided. See `the SciPy documentation
<https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html>`_
for more details and options.

While the default method converges quickly and often yields acceptable fits,
the results may be sensitive to the initial conditions.
EIS fitting can be prone to this issue given the high dimensionality
of typical equivalent circuit models.
`Global optimization algorithms <https://en.wikipedia.org/wiki/Global_optimization>`_
attempt to search the entire parameter landscape to minimize the error.
By setting :code:`global_opt=True` in :code:`circuit_fit`, :code:`impedance.py` will use the
`basinhopping <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.basinhopping.html>`_
global optimization algorithm (also from the `scipy.optimize` package[1]) instead of :code:`curve_fit`.
Note that the computational time may increase.

[1] Virtanen, P., Gommers, R., Oliphant, T.E. et al.
SciPy 1.0: fundamental algorithms for scientific computing in Python.
Nat Methods 17, 261–272 (2020). `doi: 10.1038/s41592-019-0686-2 <https://doi.org/10.1038/s41592-019-0686-2>`_

How do I cite impedance.py?
---------------------------

.. image:: https://joss.theoj.org/papers/10.21105/joss.02349/status.svg
    :target: https://doi.org/10.21105/joss.02349

If you use impedance.py in published work, please consider citing https://joss.theoj.org/papers/10.21105/joss.02349 as

.. code:: text

    @article{Murbach2020,
        doi = {10.21105/joss.02349},
        url = {https://doi.org/10.21105/joss.02349},
        year = {2020},
        publisher = {The Open Journal},
        volume = {5},
        number = {52},
        pages = {2349},
        author = {Matthew D. Murbach and Brian Gerwe and Neal Dawson-Elli and Lok-kun Tsui},
        title = {impedance.py: A Python package for electrochemical impedance analysis},
        journal = {Journal of Open Source Software}
    }

How can I contribute to impedance.py?
-------------------------------------

First off, thank you for your interest in contributing to the
open-source electrochemical community! We're excited to welcome all
contributions including suggestions for new features, bug reports/fixes,
examples/documentation, and additional impedance analysis functionality.

Feature requests and bug reports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to make a suggestion for a new feature, please `make an
issue <https://github.com/ECSHackWeek/impedance.py/issues/new/choose>`_
including as much detail as possible. If you're requesting a
new circuit element or data file type, there are special issue templates
that you can select and use.

Contributing code
~~~~~~~~~~~~~~~~~

The prefered method for contributing code to impedance.py is to fork
the repository on GitHub and submit a "pull request" (PR).
More detailed information on how to get started developing impedance.py
can be found in
`CONTRBUTING.md <https://github.com/ECSHackWeek/impedance.py/blob/master/CONTRIBUTING.md>`_.

Feel free to reach out via GitHub issues with any questions!

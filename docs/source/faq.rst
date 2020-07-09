Frequently Asked Questions
==========================

What method does impedance.py use for fitting equivalent circuit models?
----------------------------------------------------------------
Fitting is performed by non-linear least squares regression of
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

[1] Virtanen, P., Gommers, R., Oliphant, T.E. et al.
SciPy 1.0: fundamental algorithms for scientific computing in Python.
Nat Methods 17, 261–272 (2020). `doi: 10.1038/s41592-019-0686-2 <https://doi.org/10.1038/s41592-019-0686-2>`_

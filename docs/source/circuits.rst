Equivalent Circuit Modeling
===========================

`impedance.py` provides a simple, yet powerful interface for fitting
any custom equivalent circuit. To define a custom circuit, a string
defining the series and parallel combinations of circuit elements.

.. note::
  To specify elements in series, the elements are separated by a dash :code:`-`
  (e.g. :code:`'R0-R2'` describes two resistors in series). Parallel elements
  are specified by :code:`p(X1, X2)` (e.g. :code:`p(R1, C1)` is a resistor and
  capacitor in parallel). 

.. automodule:: impedance.models.circuits.circuits
   :members:

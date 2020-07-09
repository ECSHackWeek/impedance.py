
.. eisfit documentation master file, created by
   sphinx-quickstart on Wed May 16 16:54:07 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

impedance.py
=============

:code:`impedance.py` is a Python package for making 
electrochemical impedance spectroscopy (EIS) analysis
reproducible and easy-to-use.

Aiming to create a consistent,
`scikit-learn-like API <https://arxiv.org/abs/1309.0238>`_
for impedance analysis, :code:`impedance.py` contains
modules for data preprocessing, validation, model fitting,
and visualization.


If you have a feature request or find a bug, please 
`file an issue <https://github.com/ECSHackWeek/impedance.py/issues>`_
or, better yet, make the code improvements and 
`submit a pull request <https://help.github.com/articles/creating-a-pull-request-from-a-fork/>`_!
The goal is to build an open-source tool that the
entire impedance community can improve and use!

Installation
------------

The easiest way to install :code:`impedance.py` is
from `PyPI <https://pypi.org/project/impedance/>`_ 
using pip:

.. code-block:: bash

   pip install impedance

See :doc:`./getting-started` for instructions
on getting started from scratch.

Dependencies
~~~~~~~~~~~~

impedance.py requires:

-   Python (>=3.7)
-   SciPy (>=1.0)
-   NumPy (>=1.14)
-   Matplotlib (>=3.0)
-   Altair (>=3.0)

Several example notebooks are provided in the examples/ directory.
Opening these will require Jupyter notebook or Jupyter lab.

Examples and Documentation
---------------------------
:doc:`./getting-started` contains a detailed walk
through of how to get started from scratch. If you're already familiar with
Jupyter/Python, several examples can be found in the :code:`examples/` directory
(:doc:`./examples/fitting_example` is a great place to start). 
The documentation can be found at 
`impedancepy.readthedocs.io <https://impedancepy.readthedocs.io/en/latest/>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   getting-started
   examples
   preprocessing
   validation
   circuits
   circuit-elements
   fitting
   faq

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

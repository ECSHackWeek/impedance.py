
.. eisfit documentation master file, created by
   sphinx-quickstart on Wed May 16 16:54:07 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

impedance.py
=============

:code:`impedance.py` is a Python module for working with impedance data.

This project started at the `2018 Electrochemical Society (ECS) Hack Week
<https://www.electrochem.org/233/hack-week/>`_ and has grown from there.

Using a `scikit-learn-like API <https://arxiv.org/abs/1309.0238>`_, we hope to make visualizing, fitting, and analyzing impedance spectra more intuitive and reproducible.

.. note::
  :code:`impedance.py` is currently in a beta phase and new features are rapidly being added.
 
If you have a feature request or find a bug, please feel free to `file an issue <https://github.com/ECSHackWeek/impedance.py/issues>`_ or, better yet, make the code improvements and `submit a pull request
<https://help.github.com/articles/creating-a-pull-request-from-a-fork/>`_! The goal is to build an open-source tool that the entire impedance community can improve and use!

Dependencies
-------------
impedance.py requires:

- Python (>=3.5)
- SciPy (>=1.0)
- NumPy (>=1.14)
- Matplotlib (>=3.0)

Several example notebooks are provided in the :code:`examples/` directory. Opening these will require Jupyter notebook or Jupyter lab.

User Installation
------------------
The easiest way to install :code:`impedance.py` is from `PyPI <https://pypi.org/project/impedance/>`_ using pip:

.. code-block:: bash
   
   pip install impedance

Examples and Documentation
---------------------------
Several examples can be found in the `examples/` directory (the `fitting_tutorial.ipynb <https://github.com/ECSHackWeek/impedance.py/blob/master/docs/source/examples/fitting_example.ipynb>`_ is a great place to start) and the documentation can be found at `impedancepy.readthedocs.io <https://impedancepy.readthedocs.io/en/latest/>`_.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   examples
   circuits
   fitting
   validation
   preprocessing


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

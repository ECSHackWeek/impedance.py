[![Build Status](https://travis-ci.org/ECSHackWeek/impedance.py.svg?branch=master)](https://travis-ci.org/ECSHackWeek/impedance.py)

[![Coverage Status](https://coveralls.io/repos/github/ECSHackWeek/impedance.py/badge.svg?branch=master)](https://coveralls.io/github/ECSHackWeek/impedance.py?branch=master)

[![Documentation Status](https://readthedocs.org/projects/impedancepy/badge/?version=latest)](https://impedancepy.readthedocs.io/en/latest/?badge=latest)

impedance.py
------------

`impedance.py` is a Python module for working with impedance data.

This project started at the [2018 Electrochemical Society (ECS) Hack Week in Seattle](https://www.electrochem.org/233/hack-week) and has grown from there.

Using a [scikit-learn-like API](https://arxiv.org/abs/1309.0238), we hope to make visualizing, fitting, and analyzing impedance spectra more intuitive and reproducible.

<i>impedance.py is currently in the alpha phase and new features are rapidly being added.</i>
If you have a feature request or find a bug, please feel free to [file an issue](https://github.com/ECSHackWeek/impedance.py/issues) or, better yet, make the code improvements and [submit a pull request](https://help.github.com/articles/creating-a-pull-request-from-a-fork/)! The goal is to build an open-source tool that the entire impedance community can improve and use!

impedance.py currently provides:
- a simple API for fitting, predicting, and plotting impedance
- equivalent circuit fitting with customizable models
- convenient Nyquist plots including confidence interval estimation for fit circuits

several features are currently being improved upon:
- implementation of measurement models as a data validation method
- interactive plotting with altair
- adding more impedance elements
- physics-based impedance models for lithium-ion batteries

### Installation
#### Dependencies

impedance.py requires:

- Python (>=3.5)
- SciPy (>=1.0)
- NumPy (>=1.14)
- Matplotlib (>=2.2)

Several example notebooks are provided in the examples/jupyter directory. Opening these will require Jupyter notebook or Jupyter lab.

#### User Installation

If you already have a working installation of numpy, scipy, and matplotlib, the easiest way to install impedance.py is using pip:

`pip install -U impedance`

#### Examples and Documentation

Several examples can be found in the `examples/` directory and the documentation can be found at [impedancepy.readthedocs.io](https://impedancepy.readthedocs.io/en/latest/). 

[![Build Status](https://travis-ci.org/ECSHackWeek/impedance.py.svg?branch=master&kill_cache=1)](https://travis-ci.org/ECSHackWeek/impedance.py)

[![Coverage Status](https://coveralls.io/repos/github/ECSHackWeek/impedance.py/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/ECSHackWeek/impedance.py?branch=master)

[![Documentation Status](https://readthedocs.org/projects/impedancepy/badge/?version=latest&kill_cache=1)](https://impedancepy.readthedocs.io/en/latest/?badge=latest)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cd7e6ee6f638458bb1bc9e1cab025409)](https://www.codacy.com/app/mdmurbach/impedance.py?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ECSHackWeek/impedance.py&amp;utm_campaign=Badge_Grade)

impedance.py
------------

`impedance.py` is a Python module for working with impedance data.

This project started at the [2018 Electrochemical Society (ECS) Hack Week in Seattle](https://www.electrochem.org/233/hack-week) and has grown from there.

Using a [scikit-learn-like API](https://arxiv.org/abs/1309.0238), we hope to make visualizing, fitting, and analyzing impedance spectra more intuitive and reproducible.

<i>impedance.py is currently in a beta phase and new features are rapidly being added.</i>
If you have a feature request or find a bug, please feel free to [file an issue](https://github.com/ECSHackWeek/impedance.py/issues) or, better yet, make the code improvements and [submit a pull request](https://help.github.com/articles/creating-a-pull-request-from-a-fork/)! The goal is to build an open-source tool that the entire impedance community can improve and use!

impedance.py currently provides:
-   a simple API for fitting, predicting, and plotting impedance
-   validation methods for checking measurement validity
-   equivalent circuit fitting with customizable models
-   convenient Nyquist plots including confidence interval estimation for fit circuits

several features are currently being improved upon:
-   interactive plotting with altair
-   physics-based impedance models for lithium-ion batteries

### Installation
#### Dependencies

impedance.py requires:

-   Python (>=3.5)
-   SciPy (>=1.0)
-   NumPy (>=1.14)
-   Matplotlib (>=3.0)

Several example notebooks are provided in the examples/ directory. Opening these will require Jupyter notebook or Jupyter lab.

#### User Installation

The easiest way to install impedance.py is from [PyPI](https://pypi.org/project/impedance/) using pip (see [`Getting started with impedance.py`](https://impedancepy.readthedocs.io/en/latest/getting-started.html) for instructions).

#### Examples and Documentation

Several examples can be found in the `examples/` directory (the [fitting_tutorial.ipynb](https://github.com/ECSHackWeek/impedance.py/blob/master/docs/source/examples/fitting_example.ipynb) is a great place to start) and the documentation can be found at [impedancepy.readthedocs.io](https://impedancepy.readthedocs.io/en/latest/).

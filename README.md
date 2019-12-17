![GitHub release](https://img.shields.io/github/release/ECSHackWeek/impedance.py) ![PyPI - Downloads](https://img.shields.io/pypi/dm/impedance?style=flat-square)
[![All Contributors](https://img.shields.io/badge/all_contributors-11-orange.svg?style=flat-square)](#contributors)

[![Build Status](https://travis-ci.org/ECSHackWeek/impedance.py.svg?branch=master&kill_cache=1)](https://travis-ci.org/ECSHackWeek/impedance.py) [![Documentation Status](https://readthedocs.org/projects/impedancepy/badge/?version=latest&kill_cache=1)](https://impedancepy.readthedocs.io/en/latest/?badge=latest)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cd7e6ee6f638458bb1bc9e1cab025409)](https://www.codacy.com/app/mdmurbach/impedance.py?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ECSHackWeek/impedance.py&amp;utm_campaign=Badge_Grade) [![Coverage Status](https://coveralls.io/repos/github/ECSHackWeek/impedance.py/badge.svg?branch=master&kill_cache=1)](https://coveralls.io/github/ECSHackWeek/impedance.py?branch=master)

impedance.py
------------

`impedance.py` is a Python module for working with impedance data.

This project started at the [2018 Electrochemical Society (ECS) Hack Week in Seattle](https://www.electrochem.org/233/hack-week) and has grown from there.

Using a [scikit-learn-like API](https://arxiv.org/abs/1309.0238), we hope to make visualizing, fitting, and analyzing impedance spectra more intuitive and reproducible.

<i>impedance.py is currently under development and new features are rapidly being added.</i>
If you have a feature request or find a bug, please feel free to [file an issue](https://github.com/ECSHackWeek/impedance.py/issues) or, better yet, make the code improvements and [submit a pull request](https://help.github.com/articles/creating-a-pull-request-from-a-fork/)! The goal is to build an open-source tool that the entire impedance community can improve and use!

impedance.py currently provides:
-   [preprocessing functions](https://impedancepy.readthedocs.io/en/latest/preprocessing.html) for easily loading in impedance data from a wide variety of file types
-   a simple API for fitting, predicting, and plotting impedance
-   [validation methods](https://impedancepy.readthedocs.io/en/latest/validation.html) for checking measurement validity
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

The easiest way to install impedance.py is from [PyPI](https://pypi.org/project/impedance/) using pip (see [Getting started with impedance.py](https://impedancepy.readthedocs.io/en/latest/getting-started.html) for instructions).

#### Examples and Documentation

Several examples can be found in the `examples/` directory (the [fitting_tutorial.ipynb](https://github.com/ECSHackWeek/impedance.py/blob/master/docs/source/examples/fitting_example.ipynb) is a great place to start) and the documentation can be found at [impedancepy.readthedocs.io](https://impedancepy.readthedocs.io/en/latest/).

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/lktsui"><img src="https://avatars0.githubusercontent.com/u/22246069?v=4" width="100px;" alt=""/><br /><sub><b>Lok-kun Tsui</b></sub></a><br /><a href="https://github.com/ECSHackWeek/impedance.py/commits?author=lktsui" title="Code">💻</a> <a href="https://github.com/ECSHackWeek/impedance.py/commits?author=lktsui" title="Tests">⚠️</a> <a href="https://github.com/ECSHackWeek/impedance.py/commits?author=lktsui" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/BGerwe"><img src="https://avatars3.githubusercontent.com/u/38819321?v=4" width="100px;" alt=""/><br /><sub><b>Brian Gerwe</b></sub></a><br /><a href="https://github.com/ECSHackWeek/impedance.py/commits?author=BGerwe" title="Code">💻</a> <a href="https://github.com/ECSHackWeek/impedance.py/commits?author=BGerwe" title="Tests">⚠️</a> <a href="https://github.com/ECSHackWeek/impedance.py/commits?author=BGerwe" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/nealde"><img src="https://avatars2.githubusercontent.com/u/25877868?v=4" width="100px;" alt=""/><br /><sub><b>Neal</b></sub></a><br /><a href="https://github.com/ECSHackWeek/impedance.py/pulls?q=is%3Apr+reviewed-by%3Anealde" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="http://mattmurbach.com"><img src="https://avatars3.githubusercontent.com/u/9369020?v=4" width="100px;" alt=""/><br /><sub><b>Matt Murbach</b></sub></a><br /><a href="https://github.com/ECSHackWeek/impedance.py/commits?author=mdmurbach" title="Documentation">📖</a> <a href="https://github.com/ECSHackWeek/impedance.py/pulls?q=is%3Apr+reviewed-by%3Amdmurbach" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/ECSHackWeek/impedance.py/commits?author=mdmurbach" title="Tests">⚠️</a> <a href="https://github.com/ECSHackWeek/impedance.py/commits?author=mdmurbach" title="Code">💻</a></td>
    <td align="center"><a href="https://kennyvh.com"><img src="https://avatars2.githubusercontent.com/u/29909203?v=4" width="100px;" alt=""/><br /><sub><b>Kenny Huynh</b></sub></a><br /><a href="https://github.com/ECSHackWeek/impedance.py/issues?q=author%3Ahkennyv" title="Bug reports">🐛</a> <a href="https://github.com/ECSHackWeek/impedance.py/commits?author=hkennyv" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/lawrencerenna"><img src="https://avatars0.githubusercontent.com/u/49174337?v=4" width="100px;" alt=""/><br /><sub><b>lawrencerenna</b></sub></a><br /><a href="#ideas-lawrencerenna" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/Rowin"><img src="https://avatars3.githubusercontent.com/u/1727478?v=4" width="100px;" alt=""/><br /><sub><b>Rowin</b></sub></a><br /><a href="https://github.com/ECSHackWeek/impedance.py/issues?q=author%3ARowin" title="Bug reports">🐛</a> <a href="https://github.com/ECSHackWeek/impedance.py/commits?author=Rowin" title="Code">💻</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/michaelplews"><img src="https://avatars2.githubusercontent.com/u/14098929?v=4" width="100px;" alt=""/><br /><sub><b>Michael Plews</b></sub></a><br /><a href="#ideas-michaelplews" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/Chebuskin"><img src="https://avatars0.githubusercontent.com/u/33787723?v=4" width="100px;" alt=""/><br /><sub><b>Chebuskin</b></sub></a><br /><a href="https://github.com/ECSHackWeek/impedance.py/issues?q=author%3AChebuskin" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/environmat"><img src="https://avatars0.githubusercontent.com/u/9309353?v=4" width="100px;" alt=""/><br /><sub><b>environmat</b></sub></a><br /><a href="https://github.com/ECSHackWeek/impedance.py/issues?q=author%3Aenvironmat" title="Bug reports">🐛</a></td>
    <td align="center"><a href="http://www.abdullahsumbal.com"><img src="https://avatars2.githubusercontent.com/u/12946947?v=4" width="100px;" alt=""/><br /><sub><b>Abdullah Sumbal</b></sub></a><br /><a href="https://github.com/ECSHackWeek/impedance.py/issues?q=author%3Aabdullahsumbal" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/nobkat"><img src="https://avatars3.githubusercontent.com/u/29077445?v=4" width="100px;" alt=""/><br /><sub><b>nobkat</b></sub></a><br /><a href="https://github.com/ECSHackWeek/impedance.py/commits?author=nobkat" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
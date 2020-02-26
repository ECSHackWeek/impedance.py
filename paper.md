---
title: 'impedance.py: A Python package for electrochemical impedance analysis'
tags:
  - Python
  - electrochemistry
  - impedance
  - lithium-ion batteries
  - fuel cells
  - corrosion
authors:
  - name: Matthew D. Murbach
    email: matt@hivebattery.com
    orcid: 0000-0002-6583-5995
    affiliation: 1
  - name: Brian Gerwe
    affiliation: 2
  - name: Neal Dawson-Elli
    affiliation: 3
  - name: Lok-kun Tsui
    affiliation: 4
affiliations:
 - name: Hive Battery Labs
   index: 1
 - name: University of Washington
   index: 2
 - name: PayScale, Inc.
   index: 3
 - name: University of New Mexico
   index: 4
date: 19 February 2020
bibliography: paper.bib
---

`impedance.py` is a community-driven Python package for making the analysis of electrochemical
impedance spectroscopy (EIS) data easier and more reproducible. `impedance.py` currently provides several useful features commonly used in the typical impedance analysis workflow:

- _data ingestion_: functions for importing data from a wide variety of instruments and file types
- _data validation_: easy-to-use methods for checking measurement validity
- _model fitting_: a simple and powerful interface for quickly fitting models to quickly analyze data
- _model selection_: parameter error estimates and model confidence bounds
- _visualization_: interactive Nyquist and Bode plots (via Altair[@vanderplas_altair_2018] and matplotlib[@hunter_matplotlib_2007])

# Background

Electrochemical impedance spectroscopy (EIS) is a powerful technique for noninvasively
probing the physicochemical processes governing complex electrochemical systems.
[@orazem_electrochemical_2008] To date, typical analysis of impedance spectra have relied
on either instrument-specific, proprietary software or ad hoc, lab-specific code written for internal use. By providing an open-source, community-driven package for the full impedance
analysis pipeline from data management to parameter extraction to publication ready figures,
`impedance.py` seeks to encourage reproducible, easy-to-use, and transparent analysis.

Additionally, in addition to decades of electrochemimical research, many new methods for validating[@schonleber_method_2014] and analyzing[@murbach_analysis_2018; @buteau_analysis_2019] impedance spectra have been developed by researchers. By lowering the barrier to use
tried-and-true methods along side cutting-edge analytical techniques via a consistent
interface, `impedance.py` serves to grow as a community repository of best-practices while facilitating the adoption of new techniques.

# Getting started using impedance.py

The documentation for `impedance.py` contains
[a guide on getting started](https://impedancepy.readthedocs.io/en/latest/getting-started.html)
and several examples of what a typical analysis workflow might look like
using the package.

For example, importing data, defining and fitting an equivalent circuit model, and visualizing
the results can be done with a handful of lines in `impedance.py`:

(1) loading in data:
```python
from impedance.preprocessing import readFile
f, Z = readFile('exampleData.csv')
```

(2) importing and initializing the circuit:
```python
from impedance.models.circuits import CustomCircuit
initial_guess = [1e-8, .01, .005, .1, .9, .005, .1, .9, .1, 200]
circuit = CustomCircuit('L0-R0-p(R1,E1)-p(R2,E2)-W1',
                        initial_guess=initial_guess)
```

(3) fitting the circuit to the data
```python
circuit.fit(f, Z)
```

and (4) visualize the results
```python
circuit.plot()
```

![Interactive impedance plots are as easy as `.plot()`!](./docs/source/examples/example.png)

# Acknowledgements

We thank participants on the 2018 Electrochemical Society (ECS) Hack Week team
in Seattle, WA as well as Dan Schwartz and David Beck for their guidance.
An up-to-date [list of contributors can be found on GitHub](https://github.com/ECSHackWeek/impedance.py#contributors-).

# References

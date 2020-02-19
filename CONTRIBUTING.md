:tada: Welcome to the open-source impedance analysis community! :tada:

Everyone is welcome to contribute.
We value all forms of contributions including code reviews, bug fixes, new features, examples, documentation, community participation, etc.

This document outlines the guidelines for contributing to the various aspects of the project.

# Contributing

If you find a bug in the code or a mistake in the [documentation](https://impedancepy.readthedocs.io/en/latest/?badge=latest) or want a new feature, you can help us by creating [an issue in our repository](https://github.com/ECSHackWeek/impedance.py/issues), or even submit a pull request.

# Development Guide

## Repository Setup

1.  To work on the impedance.py package, you should first fork the repository on GitHub using the button on the top right of the ECSHackWeek/impedance.py repository.

2.  You can then clone the fork to your computer

```bash
git clone https://github.com/<GitHubUsername>/impedance.py
```

3.  Make your changes and commit them to your fork (for an introduction to git, checkout the [tutorial from the ECS Hack Week](https://github.com/ECSHackWeek/ECSHackWeek_Dallas/blob/master/Version_Control.pptx))

For example,
```bash
git add changedfiles
git commit
git push
```

4.  [Submit a Pull Request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests) (make sure to write a good message so the reviewer can understand what you're adding!) via GitHub.

5.  Add yourself to the list of collaborators (you can use the [all-contributors bot](https://allcontributors.org/docs/en/bot/usage))! You rock!

## Continuous Integration

`impedance.py` uses [Travis CI](https://travis-ci.org/ECSHackWeek/impedance.py) for Continuous Integration testing. This means that every time you submit a pull request, a series of tests will be run to make sure the changes don’t accidentally introduce any bugs :bug:. *Your PR will not be accepted until it passes all of these tests.* While you can certainly wait for the results of these tests after submitting a PR, you can also run them locally to speed up the review process.

We use flake8 to test for PEP 8 conformance. [PEP 8](https://www.python.org/dev/peps/pep-0008/) is a series of style guides for Python that provide suggestions for everything from variable naming to indentation. 
To run the flake8 (PEP8) code style checker:

```
conda install flake8
cd impedance.py/
flake8
```
:warning: if there is any output here, fix the errors and try running flake8 again.

To run the tests using py.test:

```
conda install pytest
cd impedance.py/
pytest
```
:warning: you should see all tests pass, if not try fixing the error or file an issue.

### Unit Tests

`impedance.py` aims to have complete test coverage of our package code. If you're adding a new feature, consider writing the test first and then the code to ensure it passes. PRs which decrease code coverage will need to add tests before they can be merged.

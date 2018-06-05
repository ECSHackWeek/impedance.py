import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="impedance",
    version="0.1.0-alpha",
    author="impedance.py developers",
    author_email="mmurbach@uw.edu",
    description="A Python package for working with impedance data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://impedancepy.readthedocs.io/en/latest/",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

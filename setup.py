from impedance import __version__
import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="impedance",
    version=__version__,
    author="impedance.py developers",
    author_email="matt.murbach@gmail.com",
    description="A package for analyzing electrochemical impedance data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://impedancepy.readthedocs.io/en/latest/",
    packages=setuptools.find_packages(),
    python_requires="~=3.6",
    install_requires=['altair>=3.0', 'matplotlib>=3.0',
                      'numpy>=1.14', 'scipy>=1.0'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

"""
Methods for preprocessing impedance data from instrument files
"""

import numpy as np


def readFile(filename, instrument=None):
    """ A wrapper for reading in many common types of impedance files

    Parameters
    ----------
    filename: string
        Filename to extract impedance data from
    instrument: string
        Type of instrument file

    Returns
    -------
    frequencies : np.ndarray
        Array of frequencies
    impedance : np.ndarray of complex numbers
        Array of complex impedances

    """

    supported_types = ['gamry', 'autolab', 'parstat']

    if instrument is not None:
        assert instrument in supported_types,\
            '{} is not a supported instrument ({})'.format(instrument,
                                                           supported_types)

    if instrument == 'gamry':
        f, Z = readGamry(filename)
    elif instrument == 'autolab':
        f, Z = readAutolab(filename)
    elif instrument == 'parstat':
        f, Z = readParstat(filename)
    elif instrument is None:
        f, Z = readCSV(filename)

    return f, Z


def readGamry(filename):
    """ function for reading the .DTA file from Gamry

    Parameters
    ----------
    filename: string
        Filename of .DTA file to extract impedance data from

    Returns
    -------
    frequencies : np.ndarray
        Array of frequencies
    impedance : np.ndarray of complex numbers
        Array of complex impedances

    """

    with open(filename, 'r', encoding='ISO-8859-1') as input_file:
        lines = input_file.readlines()

    for i, line in enumerate(lines):
        if 'ZCURVE' in line:
            start_line = i

    raw_data = lines[start_line + 3:]
    f, Z = [], []
    for line in raw_data:
        each = line.split()
        f.append(float(each[2]))
        Z.append(complex(float(each[3]), float(each[4])))

    return np.array(f), np.array(Z)


def readAutolab(filename):
    """ function for reading the .csv file from Autolab

    Parameters
    ----------
    filename: string
        Filename of .csv file to extract impedance data from

    Returns
    -------
    frequencies : np.ndarray
        Array of frequencies
    impedance : np.ndarray of complex numbers
        Array of complex impedances

    """

    with open(filename, 'r') as input_file:
        lines = input_file.readlines()

    raw_data = lines[1:]
    f, Z = [], []
    for line in raw_data:
        each = line.split(',')
        f.append(each[0])
        Z.append(complex(float(each[1]), float(each[2])))

    return np.array(f), np.array(Z)


def readParstat(filename):
    """ function for reading the .txt file from Parstat

    Parameters
    ----------
    filename: string
        Filename of .txt file to extract impedance data from

    Returns
    -------
    frequencies : np.ndarray
        Array of frequencies
    impedance : np.ndarray of complex numbers
        Array of complex impedances

    """

    with open(filename, 'r') as input_file:
        lines = input_file.readlines()

    raw_data = lines[1:]
    f, Z = [], []
    for line in raw_data:
        each = line.split()
        f.append(each[4])
        Z.append(complex(float(each[6]), float(each[7])))

    return np.array(f), np.array(Z)


def readCSV(filename):
    data = np.genfromtxt(filename, delimiter=',')

    f = data[:, 0]
    Z = data[:, 1] + 1j*data[:, 2]

    return f, Z

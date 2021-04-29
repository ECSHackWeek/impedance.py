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

    supported_types = ['gamry', 'autolab', 'parstat', 'zplot', 'versastudio',
                       'powersuite', 'biologic', 'chinstruments']

    if instrument is not None:
        assert instrument in supported_types,\
            '{} is not a supported instrument ({})'.format(instrument,
                                                           supported_types)

    if instrument == 'gamry':
        f, Z = readGamry(filename)
    elif instrument == 'autolab':
        f, Z = readAutolab(filename)
    elif instrument == 'biologic':
        f, Z = readBioLogic(filename)
    elif instrument == 'parstat':
        f, Z = readParstat(filename)
    elif instrument == 'zplot':
        f, Z = readZPlot(filename)
    elif instrument == 'versastudio':
        f, Z = readVersaStudio(filename)
    elif instrument == 'powersuite':
        f, Z = readPowerSuite(filename)
    elif instrument == 'chinstruments':
        f, Z = readCHInstruments(filename)
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

    end_line = 0

    for i, line in enumerate(lines):
        if 'ZCURVE' in line:
            start_line = i
        if 'EXPERIMENTABORTED' in line:
            end_line = i

    if end_line != 0:
        raw_data = lines[start_line + 3:end_line]
    else:
        raw_data = lines[start_line + 3:]

    f, Z = [], []
    for line in raw_data:
        each = line.split()
        f.append(float(each[2]))
        Z.append(complex(float(each[3]), float(each[4])))

    return np.array(f), np.array(Z)


def readAutolab(filename):
    """ function for reading comma-delimited files from Autolab

    Parameters
    ----------
    filename: string
        Filename of file to extract impedance data from

    Returns
    -------
    frequencies : np.ndarray
        Array of frequencies
    impedance : np.ndarray of complex numbers
        Array of complex impedances

    """

    with open(filename, 'r', encoding="utf8") as input_file:
        lines = input_file.readlines()

    for i, line in enumerate(lines):
        if line.find('Freq') != -1:
            start_line = i

    raw_data = lines[start_line+1:]
    f, Z = [], []
    for line in raw_data:
        each = line.split(',')
        f.append(float(each[0]))
        Z.append(complex(float(each[4]), float(each[5])))

    return np.array(f), np.array(Z)


def readBioLogic(filename):
    """ function for reading the .mpt file from Biologic
        EC-lab software

        Parameters
        ----------
        filename: string
            Filename of .mpt file to extract impedance data from

        Returns
        -------
        frequencies : np.ndarray
            Array of frequencies
        impedance : np.ndarray of complex numbers
            Array of complex impedances

        """

    with open(filename, 'r', encoding="latin-1") as input_file:
        lines = input_file.readlines()

    header_line = lines[1]

    # MPT data format has variable number of header lines
    number_header_lines = int(header_line.split(":")[1])

    # find the freq and Z columns
    headers = lines[number_header_lines-1].split('\t')

    freq_cols = [o for o, h in enumerate(headers) if h == 'freq/Hz']
    ReZ_cols = [o for o, h in enumerate(headers) if h == 'Re(Z)/Ohm']
    ImZ_cols = [o for o, h in enumerate(headers) if h == '-Im(Z)/Ohm']

    col_heads = ['freq/Hz', 'Re(Z)/Ohm', '-Im(Z)/Ohm']
    for cols, ch in zip([freq_cols, ReZ_cols, ImZ_cols], col_heads):
        assert len(cols) > 0, f'"{ch}" not found in column headers'

    freq_col = freq_cols[0]
    ReZ_col = ReZ_cols[0]
    ImZ_col = ImZ_cols[0]

    raw_data = lines[number_header_lines:]
    f, Z = [], []
    for line in raw_data:
        each = line.split('\t')
        f.append(float(each[freq_col]))

        # MPT data format saves the imaginary portion as -Im(Z) not Im(Z)
        Z.append(complex(float(each[ReZ_col]), -1*float(each[ImZ_col])))

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
        if float(each[3]) != 0:
            f.append(float(each[3]))
            Z.append(complex(float(each[4]), float(each[5])))

    return np.array(f), np.array(Z)


def readVersaStudio(filename):
    """ function for reading the .PAR file from VersaStudio

    Parameters
    ----------
    filename: string
        Filename of .PAR file to extract impedance data from

    Returns
    -------
    frequencies : np.ndarray
        Array of frequencies
    impedance : np.ndarray of complex numbers
        Array of complex impedances

    """
    from re import split
    with open(filename, 'r', encoding="utf8") as input_file:
        lines = input_file.readlines()

    # List to track [segment index, segment start line, segment end line]
    segments = list([])

    for i, line in enumerate(lines):
        if "Segments" in line:
            if not segments:
                segments = [[int(j) for j in split(r'[=\n]', line)
                            if j.isdigit()]]

            elif [int(j) for j in split(r'[=\n]', line) if j.isdigit()]:
                segments.append([int(j) for j in split(r'[=\n]', line)
                                if j.isdigit()])

        if segments:
            for j in segments:
                if '<Segment' + str(segments[j[0]][0]) + '>' in line:
                    segments[j[0]].append(i)
                if '</Segment' + str(segments[j[0]][0]) + '>' in line:
                    segments[j[0]].append(i)

    # Started building for option of multiple segments,
    # but that may be an unlikely scenario
    # For the time being, assume only 1 segment of actual data (Segment1)
    # Removing segments without apparent data
    # for i in segments:
    #     if np.size(i)==1:
    #         segments.remove(i)
    # for i in segments:
    #     data_dum=lines[i[1]+4:i[2]]
    #     f, Z= [], []
    #     for line in data_dum:
    #         each=line.split(',')
    #         f.append(float(each[9]))
    #         Z.append(complex(float(each[14]),float(each[15])))

    raw_data = lines[segments[1][1]+4:segments[1][2]]
    f, Z = [], []

    for line in raw_data:
        each = line.split(',')
        f.append(float(each[9]))
        Z.append(complex(float(each[14]), float(each[15])))

    return np.array(f), np.array(Z)


def readZPlot(filename):
    """ function for reading the .z file from Scribner's ZPlot

    Parameters
    ----------
    filename: string
        Filename of .z file to extract impedance data from

    Returns
    -------
    frequencies : np.ndarray
        Array of frequencies
    impedance : np.ndarray of complex numbers
        Array of complex impedances

    """
    import re
    with open(filename, 'r', encoding="utf8") as input_file:
        lines = input_file.readlines()

    for i, line in enumerate(lines):
        # For files that have metadata in the header
        if "End Comments" in line:
            start_line = i
        # For files without metadata
        if "Freq(Hz)" in line:
            head_line = i

    try:
        raw_data = lines[start_line+1:]
    except UnboundLocalError:
        raw_data = lines[head_line+1:]

    f, Z = [], []
    for line in raw_data:
        # Can use this approach if we don't mind importing re module
        each = re.split('\t|, ', line)
        f.append(float(each[0]))
        Z.append(complex(float(each[4]), float(each[5])))
    return np.array(f), np.array(Z)


def readPowerSuite(filename):
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
        if not line.isspace():
            freq, z_re, z_im = line.split('\t')
            f.append(float(freq))
            Z.append(complex(float(z_re), float(z_im)))

    return np.array(f), np.array(Z)


def readCHInstruments(filename):
    """ function for reading the .txt file from CHInstruments

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

    # Locate the line where the data lives
    for i, line in enumerate(lines):
        if line.startswith('Freq/Hz'):
            # CH instruments has an empty space b/w header
            # and start of data line
            start_line = i+2

    raw_data = lines[start_line:]
    f, Z = [], []
    for line in raw_data:
        each = line.split(',')
        f.append(float(each[0]))
        Z.append(complex(float(each[1]), float(each[2])))

    return np.array(f), np.array(Z)


def readCSV(filename):
    """ function for reading plain csv files

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
    data = np.genfromtxt(filename, delimiter=',')

    f = data[:, 0]
    Z = data[:, 1] + 1j*data[:, 2]

    return f, Z


def saveCSV(filename, frequencies, impedances, **kwargs):
    """ saves frequencies and impedances to a csv

    Parameters
    ----------
    filename: string
        Filename of .csv file to save impedance data to
    frequencies : np.ndarray
        Array of frequencies
    impedance : np.ndarray of complex numbers
        Array of complex impedances
    kwargs :
        Keyword arguments passed to np.savetxt
    """
    if not filename.endswith('.csv'):
        filename += '.csv'

    data = np.vstack([frequencies,
                      np.real(impedances),
                      np.imag(impedances),
                      ]).T

    header = 'freq,Re(Z),Im(Z)'

    np.savetxt(filename, data, delimiter=',',
               header=header, **kwargs)


def ignoreBelowX(frequencies, Z):
    """
    Trim out all data points below the X-axis


    Parameters
    ----------
    frequencies : np.ndarray
        Array of frequencies
    Z : np.ndarray of complex numbers
        Array of complex impedances

    Returns
    -------
    frequencies : np.ndarray
        Array of frequencies after filtering
    Z : np.ndarray of complex numbers
        Array of complex impedances after filtering
    """

    frequencies = frequencies[np.imag(Z) < 0]
    Z = Z[np.imag(Z) < 0]
    return frequencies, Z


def cropFrequencies(frequencies, Z, freqmin=0, freqmax=None):
    """
    Trim out all data points below the X-axis


    Parameters
    ----------
    frequencies : np.ndarray
        Array of frequencies
    Z : np.ndarray of complex numbers
        Array of complex impedances
    freqmin : float
        Minimum frequency, omit for no lower frequency limit
    freqmax : float
        Max frequency, omit for no upper frequency limit


    Returns
    -------
    frequencies_final : np.ndarray
        Array of frequencies after filtering
    Z_final : np.ndarray of complex numbers
        Array of complex impedances after filtering
    """

    frequencies_min = frequencies[frequencies >= freqmin]
    Z_min = Z[frequencies >= freqmin]

    # If no maximum is specified, return only samples filtered by minimum
    if freqmax:
        frequencies_final = frequencies_min[frequencies_min <= freqmax]
        Z_final = Z_min[frequencies_min <= freqmax]
    else:
        frequencies_final = frequencies_min
        Z_final = Z_min

    return frequencies_final, Z_final

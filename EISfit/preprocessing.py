#import os
#from sys import *


def read_Gamry(filename):
    """ function for reading the .DTA file from Gamry

    Input
    -----------------
    filename: 
        example: test1.DTA
    
    Returns
    ------------
    frequencies : list of floats
    
    impedance : list of complex numbers
        Z = real + imag * 1j

    Notes
    ---------


    """

    INPUT = open(filename,'r',encoding = 'ISO-8859-1')
    lines = INPUT.readlines()
    INPUT.close()
    n = -1
    for line in lines:
        n = n + 1
        if 'ZCURVE' in line:
            start_line = n  
    raw_data = lines[int(start_line)+3:]  
    Freq = []
    Z = []
    for line in raw_data:
        each = line.split()
        Freq.append(float(each[2]))
        Z.append(complex(float(each[3]), float(each[4])))
    return Freq, Z

def read_Autolab(filename):
    """ function for reading the .csv file from Autolab

    Input
    -----------------
    filename: 
        example: test2.csv
    
    Returns
    ------------
    frequencies : list of floats
    
    impedance : list of complex numbers
        Z = real + imag * 1j

    Notes
    ---------


    """


    INPUT = open(filename,'r')
    lines = INPUT.readlines()
    INPUT.close()
    raw_data = lines[1:]
    Freq = []
    Z = []
    for line in raw_data:
        each = line.split(',')
        Freq.append(each[0])
        Z.append(complex(float(each[1]),float(each[2])))
    return Freq, Z

def read_Parstat(filename):
    """ function for reading the .txt file from Parstat

    Input
    -----------------
    filename: 
        example: test3.txt
    
    Returns
    ------------
    frequencies : list of floats
    
    impedance : list of complex numbers
        Z = real + imag * 1j

    Notes
    ---------


    """
    
    INPUT = open(filename,'r')
    lines = INPUT.readlines()
    INPUT.close()
    raw_data = lines[1:]
    Freq = []
    Z = []
    for line in raw_data:
        each = line.split()
        Freq.append(each[4])
        Z.append(complex(float(each[6]),float(each[7])))
    return Freq, Z





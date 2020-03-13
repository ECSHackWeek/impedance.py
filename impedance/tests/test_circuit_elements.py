import string
import numpy as np

from impedance.models.circuits.elements import circuit_elements, s, p

letters = string.ascii_uppercase + string.ascii_lowercase


def test_all():
    freqs = [0.001, 1.0, 1000]
    correct_vals = {'R': [0.1, 0.1, 0.1],
                    'C': [-1591.5494309189532j,
                          -1.5915494309189535j,
                          -0.0015915494309189533j],
                    'L': [0.000628319j, 0.628319j, 628.319j],
                    'W': [(0.033333332999112786-79.57747433847442j),
                          (0.03300437046673635-0.08232866785870396j),
                          (0.0019947114020071634-0.0019947114020071634j)],
                    'A': [(1.26156626-1.26156626j),
                          (0.03989423-0.03989423j),
                          (0.00126157-0.00126157j)],
                    'E': [(26.216236841407248-8.51817171087997j),
                          (6.585220960717244-2.139667994182814j),
                          (1.6541327179718126-0.537460300252313j)],
                    'G': [(0.09999994078244179-0.00006283179105931961j),
                          (0.07107755021941357-0.03427465211788068j),
                          (0.00199550459845528-0.0019939172581851707j)],
                    'T': [(1.00041-0.00837309j),
                          (0.0156037-0.114062j),
                          (0.00141056-0.00141039j)],
                    'RR': [10, 10, 10],
                    'K': [(0.099999842086579 - 0.000125663507704j),
                          (0.038772663673915 - 0.048723166143232j),
                          (6.332569967499333e-08 - 7.957742115295703e-05j)]}
    input_vals = [0.1, 0.2, 0.3, 0.4]
    inputs = {'R': 1,
              'C': 1,
              'L': 1,
              'W': 2,
              'A': 1,
              'E': 2,
              'G': 2,
              'T': 4,
              'RR': 1,
              'K': 2}
    for key, f in circuit_elements.items():
        # don't test the outputs of series and parallel functions
        print(key)
        print(circuit_elements)
        if key not in ['s', 'p']:
            val = f(input_vals[:inputs[key]], freqs)
            print(f.__name__, val, correct_vals[key])
            print(np.isclose(val, correct_vals[key]).all())
            assert np.isclose(val, correct_vals[key]).all()

        # check for typing:
        try:
            f = circuit_elements['R']
            f(1, 2)
        except(AssertionError):
            pass
        else:
            raise Exception('unhandled error occurred')
        # test for handling more wrong inputs
        try:
            f(['hi'], ['yes', 'hello'])
        except(AssertionError):
            pass
        else:
            raise Exception('unhandled error occurred')


def test_s():
    a = np.array([5 + 6*1j, 2 + 3*1j])
    b = np.array([5 + 6*1j, 2 + 3*1j])

    answer = np.array([10 + 12*1j, 4 + 6*1j])
    assert np.isclose(s([a, b]), answer).all()


def test_p():
    a = np.array([5 + 6*1j, 2 + 3*1j])
    b = np.array([5 + 6*1j, 2 + 3*1j])

    answer = np.array([2.5 + 3*1j, 1 + 1.5*1j])
    assert np.isclose(p([a, b]), answer).all()


def test_element_function_names():
    # run a simple check to ensure there are no integers
    # in the function names
    for elem in circuit_elements.keys():
        for char in elem:
            assert char in letters, \
                '{} in element {} is not in the allowed set of {}'.format(char, elem, letters) # noqa

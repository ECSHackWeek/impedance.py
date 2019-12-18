from impedance.circuit_elements import R, C, L, W, A, E, G, T, s, p
import numpy as np


def test_all():
    funcs = [R, C, L, W, A, E, G, T]
    freqs = [0.001, 1.0, 1000]
    correct_vals = [[0.1, 0.1, 0.1],
                    [-1591.5494309189532j,
                     -1.5915494309189535j,
                     -0.0015915494309189533j],
                    [0.000628319j, 0.628319j, 628.319j],
                    [(0.033333332999112786-79.57747433847442j),
                     (0.03300437046673635-0.08232866785870396j),
                     (0.0019947114020071634-0.0019947114020071634j)],
                    [(1.26156626-1.26156626j),
                     (0.03989423-0.03989423j),
                     (0.00126157-0.00126157j)],
                    [(26.216236841407248-8.51817171087997j),
                     (6.585220960717244-2.139667994182814j),
                     (1.6541327179718126-0.537460300252313j)],
                    [(0.09999994078244179-0.00006283179105931961j),
                     (0.07107755021941357-0.03427465211788068j),
                     (0.00199550459845528-0.0019939172581851707j)],
                    [(1.00041-0.00837309j),
                    (0.0156037-0.114062j),
                    (0.00141056-0.00141039j)]]
    input_vals = [0.1, 0.2, 0.3, 0.4]
    inputs = [1, 1, 1, 2, 1, 2, 2, 4]
    for i, f in enumerate(funcs):
        val = f(input_vals[:inputs[i]], freqs)
        print(f.__name__, val, correct_vals[i])
        print(np.isclose(val, correct_vals[i]).all())
        assert np.isclose(val, correct_vals[i]).all()

        # check for typing:
        try:
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

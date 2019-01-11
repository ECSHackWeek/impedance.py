from impedance.validation import calc_mu


def test_calc_mu():
    Rs = [1, 2, 3, -3, -2, -1]
    assert calc_mu(Rs) == 0

    Rs = [-1, 2, 4, -3, 4, -1]
    assert calc_mu(Rs) == 0.5

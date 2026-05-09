'''
Compares new buildCircuit with older buildCircuit
R0-p(R1-Wo1,CPE1) : 82.97% faster
R0-p(C1,R1,R2) : 79.30% faster
R0-p(p(R1, C1)-R2, C2) : 82.17% faster
p(C1,R1)-p(C2,R2) : 81.10% faster
R1 : 85.55% faster
'''

from impedance.models.circuits.fitting import wrapCircuit as wrapCircuit_new
from impedance.tests.fitting_org import wrapCircuit as wrapCircuit_org
import numpy as np
import time


def test_newbuildCircuit():
    data=[
        # Test simple Randles circuit with CPE,
        ('R0-p(R1-Wo1,CPE1)', [.1, .01, 1, 1000, 15, .9], [1000.0, 5.0, 0.01]), 
        # Test multiple parallel elements, 
        ('R0-p(C1,R1,R2)', [.1, .01, .2, .3], [1000.0, 5.0, 0.01]),
        # Test nested parallel groups, 
        ('R0-p(p(R1, C1)-R2, C2)', [1, 2, 3, 4, 5], [1000.0, 5.0, 0.01]),
        # Test parallel elements at beginning and end,
        ('p(C1,R1)-p(C2,R2)', [.1, .01, .2, .3], [1000.0, 5.0, 0.01]),
        # Test single element circuit, 
        ('R1', [100], [1000.0, 5.0, 0.01])
    ]
    # dt_ratio=[]
    # for circuit, params, frequencies in data:
    #     cktfn_new=wrapCircuit_new(circuit, constants={})
    #     cktfn_org=wrapCircuit_org(circuit, constants={})
    #     start = time.perf_counter()
    #     Z_org=[cktfn_org(frequencies,*params) for i in range(100)]
    #     end = time.perf_counter()
    #     dt_org = end-start
    #     start = time.perf_counter()
    #     Z_new=[cktfn_new(frequencies,*params) for i in range(100)]
    #     end = time.perf_counter()
    #     dt_new = end-start
    #     dt_ratio.append(f'{circuit} : {(1-dt_new/dt_org)*100:.2f} % faster')
    #     assert( np.isclose(Z_new[0],Z_org[0]))
    # print('\n'.join(dt_ratio))
    for circuit, params, frequencies in data:
        cktfn_new=wrapCircuit_new(circuit, constants={})
        cktfn_org=wrapCircuit_org(circuit, constants={})
        Z_org=cktfn_org(frequencies,*params)
        Z_new=cktfn_new(frequencies,*params)
        assert( np.all(np.isclose(Z_new,Z_org)) )


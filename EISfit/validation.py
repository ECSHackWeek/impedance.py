from .fitting import circuit_fit, computeCircuit, calculateCircuitLength
from .circuits import DefineCircuit
import numpy as np

def rmse(a, b):
    return(np.sqrt(np.mean(np.square(a-b))))

def measModel(frequencies, impedances, max_k = 7, R_val = 0.1, C_val = 10):
    """
    Iteratively add RC circuits until the error converges. If error does not converge, it indicates that the data is poor.
    """
    out = "R_0"
    initial_guess = [R_val]
    error_list = []
    model_list = []
    for i in range(max_k):
        out += "-p(R_{},C_{})".format(i+1,i+1)
        initial_guess.append(R_val)
        initial_guess.append(C_val)
        test = DefineCircuit(initial_guess = initial_guess,
                            circuit = out)
        print(out)
        test.fit(frequencies, impedances)
        model_list.append(test)
        fit = test.predict(frequencies)
        error = rmse(impedances, fit)
#        if i > 1 and error * 1.1 > error_list[-1] and error*0.9 < error_list[-1]:
#            break
#        else:
#            error_list.append(error)
        error_list.append(error)
        
    return [model_list, error_list]
        
        
        
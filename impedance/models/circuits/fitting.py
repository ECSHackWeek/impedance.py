import warnings

import numpy as np
from scipy.linalg import inv
from scipy.optimize import curve_fit, basinhopping

from .elements import circuit_elements, get_element_from_name

ints = '0123456789'

from warnings import warn

def rmse(a, b):
    """
    A function which calculates the root mean squared error
    between two vectors.

    Notes
    ---------
    .. math::

        RMSE = \\sqrt{\\frac{1}{n}(a-b)^2}
    """

    n = len(a)
    return np.linalg.norm(a - b) / np.sqrt(n)


def set_default_bounds(circuit, constants={}):
    """ This function sets default bounds for optimization.

    set_default_bounds sets bounds of 0 and np.inf for all parameters,
    except the CPE and La alphas which have an upper bound of 1.

    Parameters
    -----------------
    circuit : string
        String defining the equivalent circuit to be fit

    constants : dictionary, optional
        Parameters and their values to hold constant during fitting
        (e.g. {"RO": 0.1}). Defaults to {}

    Returns
    ------------
    bounds : 2-tuple of array_like
        Lower and upper bounds on parameters.
    """

    # extract the elements from the circuit
    extracted_elements = extract_circuit_elements(circuit)

    # loop through bounds
    lower_bounds, upper_bounds = [], []
    for elem in extracted_elements:
        raw_element = get_element_from_name(elem)
        for i in range(check_and_eval(raw_element).num_params):
            if elem in constants or elem + f'_{i}' in constants:
                continue
            if raw_element in ['CPE', 'La'] and i == 1:
                upper_bounds.append(1)
            else:
                upper_bounds.append(np.inf)
            lower_bounds.append(0)

    bounds = ((lower_bounds), (upper_bounds))
    return bounds


def scale_bounds(bounds,n_guess,scale):
    b0 = np.atleast_1d(bounds[0])
    b1 = np.atleast_1d(bounds[1])
    if len(b0) == 1:
        b0 = np.repeat(b0[0], n_guess)
    if len(b1) == 1:
        b1 = np.repeat(b1[0], n_guess)
    bounds = (b0, b1)
    if scale is None:
        scale = np.ones(n_guess)
    else:
        scale = np.array(scale, dtype=float)
    scaled_low = np.array(bounds[0], dtype=float) / scale
    scaled_high = np.array(bounds[1], dtype=float) / scale
    return scaled_low,scaled_high

def is_scalarval(var,val):
    if isinstance(var,(list,np.ndarray)): return False
    if var != val: return False
    return True

def circuit_fit(frequencies, impedances, circuit, initial_guess, constants={},
                bounds=None, weight_by_modulus=False, global_opt=False,
                optimizations=[], scale=None, **kwargs):

    """ Main function for fitting an equivalent circuit to data.

    By default, this function uses `scipy.optimize.curve_fit
    <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html>`_
    to fit the equivalent circuit. This function generally works well for
    simple circuits. However, the final results may be sensitive to
    the initial conditions for more complex circuits. In these cases,
    the `scipy.optimize.basinhopping
    <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.basinhopping.html>`_
    global optimization algorithm can be used to attempt a better fit.

    Parameters
    -----------------
    frequencies : numpy array
        Frequencies

    impedances : numpy array of dtype 'complex128'
        Impedances

    circuit : string
        String defining the equivalent circuit to be fit

    initial_guess : list of floats
        Initial guesses for the fit parameters

    constants : dictionary, optional
        Parameters and their values to hold constant during fitting
        (e.g. {"RO": 0.1}). Defaults to {}

    bounds : 2-tuple of array_like, optional
        Lower and upper bounds on parameters. Defaults to bounds on all
        parameters of 0 and np.inf, except the CPE alpha
        which has an upper bound of 1

    weight_by_modulus : bool, optional
        Uses the modulus of each data (|Z|) as the weighting factor.
        Standard weighting scheme when experimental variances are unavailable.
        Only applicable when global_opt = False

    global_opt : bool, optional
        If global optimization should be used (uses the basinhopping
        algorithm). Defaults to False

    optimizations : dict or list of dicts, optional
        If global_opt is True, gets set to "basinhopping"
        Else 
            If optimizations is not passed, curve_fit is used.
            If dict(s), it must algorithm + algorithm options
                "algorithm" is mandatory. eg : {"algorithm" : 'scipy_minimize', 'method' : ...} or {"algorithm" : 'pygad', 'gene_space' : ...} 
            List could be a list of dics (in the above format). This is used for sequential optimizations, particularly useful for GA.

    scale : list, optional
        Used to denote "scale" of prameters to improve convergence.
        Consider a p(R,C) or R-C circuit. Suppose C-s is in μF while, 
        R-s might be in ~0.1 ohms; we can pass [0.1,1e-6].
        Internally the parameters are divided by scale during optimization.

    kwargs :
        Keyword arguments passed to scipy.optimize.curve_fit or
        scipy.optimize.basinhopping
        One can also pass a callable soft_constraint that adds a penalty for arbitary constraints. 

    Returns
    ------------
    p_values : list of floats
        best fit parameters for specified equivalent circuit

    p_errors : list of floats
        one standard deviation error estimates for fit parameters

    Notes
    ---------
    Need to do a better job of handling errors in fitting.
    Currently, an error of -1 is returned.

    """
    kwargs_org = kwargs
    f = np.array(frequencies, dtype=float)
    Z = np.array(impedances, dtype=complex)

    # set upper and lower bounds on a per-element basis
    if bounds is None:
        bounds = set_default_bounds(circuit, constants=constants)
    wrapedCircuit=wrapCircuit(circuit, constants)

    if global_opt:
        warn('global_opt has been deprecated. Use optimizations={"algorithm" : "basinhopping"}' \
        ' OR optimizations="basinhopping"', DeprecationWarning, 2)
        opt={"algorithm" : 'basinhopping'}
        optimizations=[]
    elif optimizations == []:
        opt={"algorithm" : 'curve_fit'}
    elif isinstance(optimizations,(list)) :
        opt=optimizations.pop(0) 
    else :
        opt=optimizations
        optimizations=[]
        
    if not isinstance(opt,dict) : opt={"algorithm" : opt}

    target_Z = np.hstack([Z.real, Z.imag])
    sigma = kwargs.pop('sigma', 1)

    soft_constraint = kwargs.pop('soft_constraint', lambda p : 0)

    if opt["algorithm"] in ('scipy_minimize','pygad') or callable(opt["algorithm"]):
        if scale is None : 
            scale = 1
            warnings.warn("'scale' is recommeded for scipy_minimize...")
        scaled_low, scaled_high = scale_bounds(bounds,len(initial_guess),scale)
        def obj_fn(p_scaled):
            p_unscaled = p_scaled * scale
            try:
                pred_Z = wrapedCircuit(f, *p_unscaled)
                error =  np.sum(((pred_Z - target_Z) / sigma)**2) + soft_constraint(p_unscaled)
            except Exception:
                return np.inf
            return error
        pbar = None
        show_progress = opt.pop('show_progress', 
                    kwargs.get('show_progress', True))
        if show_progress:
            if opt["algorithm"] ==  'pygad':
                maxiter = opt.get('num_generations', 1000)
            else:
                maxiter = kwargs.get('options', {}).get('maxiter', None)
            try:
                from tqdm.auto import tqdm
                pbar = tqdm(total=maxiter, desc="circuit fit")
            except ImportError:
                warn('tqdm not found, progress cannot be plotted !!!')
    
    if opt["algorithm"] == 'curve_fit':
        if 'maxfev' not in kwargs:
            kwargs['maxfev'] = 1e5
        if 'ftol' not in kwargs:
            kwargs['ftol'] = 1e-13

        # weighting scheme for fitting
        if weight_by_modulus:
            abs_Z = np.abs(Z)
            kwargs['sigma'] = np.hstack([abs_Z, abs_Z])

        popt, pcov = curve_fit(wrapedCircuit, f,
                               target_Z,
                               p0=initial_guess, bounds=bounds, **kwargs)

        # Calculate one standard deviation error estimates for fit parameters,
        # defined as the square root of the diagonal of the covariance matrix.
        # https://stackoverflow.com/a/52275674/5144795
        perror = np.sqrt(np.diag(pcov))

    elif opt["algorithm"] == 'basinhopping':
        if 'seed' not in kwargs:
            kwargs['seed'] = 0

        def opt_function(x):
            """ Short function for basinhopping to optimize over.
            We want to minimize the RMSE between the fit and the data.

            Parameters
            ----------
            x : args
                Parameters for optimization.

            Returns
            -------
            function
                Returns a function (RMSE as a function of parameters).
            """
            return rmse(wrapedCircuit(f, *x),
                        np.hstack([Z.real, Z.imag]))

        class BasinhoppingBounds(object):
            """ Adapted from the basinhopping documetation
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.basinhopping.html
            """

            def __init__(self, xmin, xmax):
                self.xmin = np.array(xmin)
                self.xmax = np.array(xmax)

            def __call__(self, **kwargs):
                x = kwargs['x_new']
                tmax = bool(np.all(x <= self.xmax))
                tmin = bool(np.all(x >= self.xmin))
                return tmax and tmin

        basinhopping_bounds = BasinhoppingBounds(xmin=bounds[0],
                                                 xmax=bounds[1])
        results = basinhopping(opt_function, x0=initial_guess,
                               accept_test=basinhopping_bounds, **kwargs)
        popt = results.x

        # Calculate perror
        jac = results.lowest_optimization_result['jac'][np.newaxis]
        try:
            # jacobian -> covariance
            # https://stats.stackexchange.com/q/231868
            pcov = inv(np.dot(jac.T, jac)) * opt_function(popt) ** 2
            # covariance -> perror (one standard deviation
            # error estimates for fit parameters)
            perror = np.sqrt(np.diag(pcov))
        except (ValueError, np.linalg.LinAlgError):
            warnings.warn('Failed to compute perror')
            perror = None

    elif opt["algorithm"] == 'scipy_minimize':
        method = opt.pop('method', 'L-BFGS-B')
        print(f"Running {opt['algorithm']} with {method}...")

        from scipy.optimize import minimize
        user_callback = kwargs.pop('callback', None)
        def combined_callback(xk, *args, **kwds):
            if pbar is not None:
                pbar.update(1)
            if user_callback is not None:
                user_callback(xk, *args, **kwds)

        min_bounds_scaled = list(zip(scaled_low, scaled_high))
        res = minimize(obj_fn, initial_guess, bounds=min_bounds_scaled, callback=combined_callback, **kwargs)
        if pbar is not None:
            pbar.close()
        popt = res.x * scale
        if hasattr(res, 'hess_inv'):
            pcov = res.hess_inv
            if hasattr(pcov, "todense"): pcov = pcov.todense()
            pcov = pcov * np.outer(scale, scale)
        else:
            pcov = np.zeros((len(popt), len(popt)))
        perror = np.sqrt(np.diag(pcov))

    elif opt["algorithm"] == 'pygad':
        print(f"Running {opt['algorithm']}...")
        import pygad

        def fitness_func(ga_instance, solution, solution_idx):
            return 1./obj_fn(solution)

        gene_space = opt.pop('gene_space', None)
        if gene_space is None and scaled_low is not None:
            gene_space = [{'low': low, 'high': high} for low, high in zip(scaled_low, scaled_high)]

        num_generations = opt.pop('num_generations', 1000)
        num_parents_mating = opt.pop('num_parents_mating', 4)
        sol_per_pop = opt.pop('sol_per_pop', 20)
        num_genes=len(initial_guess)
        
        initial_population = opt.pop('initial_population', None)
        if initial_population is None:
            if scaled_low is None:
                raise ValueError("Bounds must be provided for PyGAD optimization to generate the initial population.")
            
            if np.any(np.isinf(scaled_low)) or np.any(np.isinf(scaled_high)):
                raise ValueError("Bounds must be finite for PyGAD optimization to generate the initial population.")
                
            initial_population = np.empty((sol_per_pop, num_genes))
            initial_population[0] = np.array(initial_guess) / scale
            
            for i in range(1, sol_per_pop):
                initial_population[i] = np.random.uniform(scaled_low, scaled_high)
                
            initial_population = np.clip(initial_population, scaled_low, scaled_high)
        else:
            initial_population = np.array(initial_population) / scale

        plot_pygad = opt.pop('plot', False)
        user_on_generation = opt.pop('on_generation', None)
            
        def on_generation(ga_instance):
            if pbar is not None:
                pbar.update(1)
            if user_on_generation:
                user_on_generation(ga_instance)

        ga_instance = pygad.GA(num_generations=num_generations,
                                num_parents_mating=num_parents_mating,
                                fitness_func=fitness_func,
                                initial_population=initial_population,
                                sol_per_pop=sol_per_pop,
                                num_genes=num_genes,
                                gene_space=gene_space,
                                on_generation=on_generation,
                                parent_selection_type=opt.pop('parent_selection_type', 'sss'), #'tournament'
                                keep_elitism=opt.pop('keep_elitism', 1),
                                **kwargs)
        ga_instance.run()
        if pbar is not None:
            pbar.close()
            
        if plot_pygad:
            ga_instance.plot_fitness()

        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        popt = solution * scale
        pcov = np.zeros((len(popt), len(popt)))        
        perror = np.sqrt(np.diag(pcov))

    elif callable(opt["algorithm"]):
        algo=opt.pop('algorithm')
        import inspect
        sig = inspect.signature(algo)
        valid_params = sig.parameters
        
        call_kwargs = {}
        # Map parameters dynamically based on the callable's signature
        if 'initial_guess' in valid_params:
            call_kwargs['initial_guess'] = initial_guess
        elif 'x0' in valid_params: # Standard scipy optimize param
            call_kwargs['x0'] = initial_guess
        else:
            warn('Initial guess was ignored')
        if 'bounds' in valid_params:
            call_kwargs['bounds'] = bounds
        else:
            warn('bounds was ignored')
        if 'scale' in valid_params:
            call_kwargs['scale'] = scale
        elif not is_scalarval(scale,1): #scale != 1 : 
            warn('scale was ignored')
        if 'fun' in valid_params:
            call_kwargs['fun'] = obj_fn
        else:
            warn('objective function was ignored (as callable does not accept "fun" parameter)')
            
        accepts_kwargs = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in valid_params.values())
        for k, v in opt.items():
            if k in valid_params or accepts_kwargs:
                call_kwargs[k] = v
                
        res = algo(**call_kwargs)
        popt = res.x if hasattr(res, 'x') else res
        pcov = np.zeros((len(popt), len(popt)))        
        perror = np.sqrt(np.diag(pcov))
    else:
        raise ValueError(f"Unknown optimization algorithm: {opt['algorithm']}")
    if len(optimizations) > 0:
        return circuit_fit(frequencies, impedances, circuit, initial_guess=popt, constants=constants,
                bounds=bounds, weight_by_modulus=weight_by_modulus, global_opt=False, optimizations=optimizations, scale=scale, **kwargs_org)
    else:
        return popt, perror

def wrapCircuit(circuit, constants):
    """ wraps function so we can pass the circuit string """
    buildCircuit_text=buildCircuit(circuit, constants=constants, 
                        eval_string='', index=0)[0]
    builtCircuit = eval('lambda frequencies,parameters : ' +  buildCircuit_text, circuit_elements)

    def wrappedCircuit(frequencies, *parameters):
        """ returns a stacked array of real and imaginary impedance
        components

        Parameters
        ----------
        circuit : string
        constants : dict
        parameters : list of floats
        frequencies : list of floats

        Returns
        -------
        array of floats

        """

        x = builtCircuit(frequencies,parameters)
        y_real = np.real(x)
        y_imag = np.imag(x)

        return np.hstack([y_real, y_imag])
    return wrappedCircuit

def buildCircuit(circuit, constants=None, eval_string='', index=0):
    """ recursive function that transforms a circuit, parameters, and
    frequencies into a string that can be evaluated

    Parameters
    ----------
    circuit: str
    frequencies: list/tuple/array of floats
    parameters: list/tuple/array of floats
    constants: dict

    Returns
    -------
    eval_string: str
        Python expression for calculating the resulting fit
        This would a string that can be used to construct a lamda function. 
        For example if circuit=R1,CPE1 with CPE1_1 = const1, eval_string = 
        "p(R(frequencies,[parameters[0]), CPE(frequencies,[p[1],const1]))"; 
        We can then construct lambda frequencies,parameters : <eval_string>

    index: int
        Tracks parameter index through recursive calling of the function
    """

    circuit = circuit.replace(' ', '')

    def parse_circuit(circuit, parallel=False, series=False):
        """ Splits a circuit string by either dashes (series) or commas
            (parallel) outside of any paranthesis. Removes any leading 'p('
            or trailing ')' when in parallel mode """

        assert parallel != series, \
            'Exactly one of parallel or series must be True'

        def count_parens(string):
            return string.count('('), string.count(')')

        if parallel:
            special = ','
            if circuit.endswith(')') and circuit.startswith('p('):
                circuit = circuit[2:-1]
        if series:
            special = '-'

        split = circuit.split(special)

        result = []
        skipped = []
        for i, sub_str in enumerate(split):
            if i not in skipped:
                if '(' not in sub_str and ')' not in sub_str:
                    result.append(sub_str)
                else:
                    open_parens, closed_parens = count_parens(sub_str)
                    if open_parens == closed_parens:
                        result.append(sub_str)
                    else:
                        uneven = True
                        while i < len(split) - 1 and uneven:
                            sub_str += special + split[i+1]

                            open_parens, closed_parens = count_parens(sub_str)
                            uneven = open_parens != closed_parens

                            i += 1
                            skipped.append(i)
                        result.append(sub_str)
        return result

    parallel = parse_circuit(circuit, parallel=True)
    series = parse_circuit(circuit, series=True)

    if series is not None and len(series) > 1:
        eval_string += "s(["
        split = series
    elif parallel is not None and len(parallel) > 1:
        eval_string += "p(["
        split = parallel
    elif series == parallel:  # only single element
        split = series

    for i, elem in enumerate(split):
        if ',' in elem or '-' in elem:
            eval_string, index = buildCircuit(elem, constants=constants,
                                              eval_string=eval_string,
                                              index=index)
        else:
            #Return a string that can be used to construct a lamda function lambda f,p : R(f,[p[0],const1,p[1]...])
            param_string = ""
            raw_elem = get_element_from_name(elem)
            elem_number = check_and_eval(raw_elem).num_params
            param_list = []
            for j in range(elem_number):
                if elem_number > 1:
                    current_elem = elem + '_{}'.format(j)
                else:
                    current_elem = elem

                if current_elem in constants.keys():
                    param_list.append(str(constants[current_elem]))
                else:
                    param_list.append(f'parameters[{index}]')
                    index += 1

            param_string = "[" + ','.join(param_list) + "]"
            new = raw_elem + '(' + param_string + ', frequencies)'
            eval_string += new

        if i == len(split) - 1:
            if len(split) > 1:  # do not add closing brackets if single element
                eval_string += '])'
        else:
            eval_string += ','

    return eval_string, index


def extract_circuit_elements(circuit):
    """ Extracts circuit elements from a circuit string.

    Parameters
    ----------
    circuit : str
        Circuit string.

    Returns
    -------
    extracted_elements : list
        list of extracted elements.

    """
    p_string = [x for x in circuit if x not in 'p(),-']
    extracted_elements = []
    current_element = []
    length = len(p_string)
    for i, char in enumerate(p_string):
        if char not in ints:
            current_element.append(char)
        else:
            # min to prevent looking ahead past end of list
            if p_string[min(i+1, length-1)] not in ints:
                current_element.append(char)
                extracted_elements.append(''.join(current_element))
                current_element = []
            else:
                current_element.append(char)
    extracted_elements.append(''.join(current_element))
    return extracted_elements


def calculateCircuitLength(circuit):
    """ Calculates the number of elements in the circuit.

    Parameters
    ----------
    circuit : str
        Circuit string.

    Returns
    -------
    length : int
        Length of circuit.

    """
    length = 0
    if circuit:
        extracted_elements = extract_circuit_elements(circuit)
        for elem in extracted_elements:
            raw_element = get_element_from_name(elem)
            num_params = check_and_eval(raw_element).num_params
            length += num_params
    return length


def check_and_eval(element):
    """ Checks if an element is valid, then evaluates it.

    Parameters
    ----------
    element : str
        Circuit element.

    Raises
    ------
    ValueError
        Raised if an element is not in the list of allowed elements.

    Returns
    -------
    Evaluated element.

    """
    allowed_elements = circuit_elements.keys()
    if element not in allowed_elements:
        raise ValueError(f'{element} not in ' +
                         f'allowed elements ({allowed_elements})')
    else:
        return eval(element, circuit_elements)

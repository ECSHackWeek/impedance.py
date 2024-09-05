import networkx as nx
import re

import numpy as np
import numdifftools as nd
from scipy.linalg import inv, norm
from scipy.optimize import curve_fit, dual_annealing, minimize, basinhopping, Bounds

from .elements import circuit_elements, get_element_from_name, format_parameter_name

ints = "0123456789"
_LBFGSB_OPTIONS = {
    "ftol": 1e-14,
    "gtol": 1e-13,
    "maxfun": 10_000,
}

_KWARGS = {
    "method": "L-BFGS-B",
    "options": _LBFGSB_OPTIONS,
}


class BoundsCheck(object):
    def __init__(self, lb, ub):
        self.lb = lb
        self.ub = ub

        if np.any(self.lb > self.ub):
            raise ValueError(
                "the lower bound must be less than or equal to the upper bound."
            )

    def __call__(self, f_new, x_new, f_old, x_old):
        return np.all(
            np.logical_and(x_new >= self.lb, x_new <= self.ub)
        ) and np.isfinite(f_new)


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
    return np.real(np.sqrt(sum_square_error(a, b) / n))


def sum_square_error(a, b, w=1):
    amb = a - b
    return np.sum(amb * np.conjugate(amb) * w)


def objective_function(graph, f, Z, weight_by_modulus=False):
    if weight_by_modulus:
        weights = 1 / norm(Z)
    else:
        weights = 1.0

    def cost_function(x):
        """Short function to optimize over.
        We want to minimize the square error between the model and the data.

        Parameters
        ----------
        x : args
            Parameters for optimization.

        Returns
        -------
        function
            Returns a function
        """
        return sum_square_error(graph(f, *x), np.stack([Z.real, Z.imag]), weights)

    return cost_function


def set_default_bounds(circuit, constants={}):
    """This function sets default bounds for optimization.

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
        for i in range(circuit_elements[raw_element].num_params):
            if elem in constants or elem + f"_{i}" in constants:
                continue
            if raw_element in ["CPE", "La"] and i == 1:
                upper_bounds.append(1)
            else:
                upper_bounds.append(np.inf)
            lower_bounds.append(0)

    bounds = ((lower_bounds), (upper_bounds))
    return bounds


def circuit_fit(
    frequencies,
    impedances,
    circuit,
    initial_guess,
    constants={},
    bounds=None,
    weight_by_modulus=False,
    global_opt=False,
    opt_method="curve_fit",
    return_covariance=False,
    **kwargs,
):
    """Main function for fitting an equivalent circuit to data.

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

    opt_method : str, optional
        What optimization method to use defaults to "curve_fit" when global_opt
        is False, but it could also be "minimize".
        When global_opt is True the default is "basinhopping", but
        "dual_annealing" is also a valid choice.

    return_covariance : bool, option
        Return the covariance matrix as well as the errors. Defaults to False.

    kwargs :
        Keyword arguments passed to scipy.optimize.curve_fit,
        scipy.optimize.minimize, scipy.optimize.dual_annealing or
        scipy.optimize.basinhopping

    Returns
    ------------
    p_values : list of floats
        best fit parameters for specified equivalent circuit

    p_errors : list of floats
        one standard deviation error estimates for fit parameters derived from
        an estimate of the covariance matrix

    p_cov : (when return_covariance is True) numpy array of floats
        estimated covariance matrix among the fit parameters

    """
    f = np.asarray(frequencies, dtype=float)
    Z = np.asarray(impedances, dtype=complex)
    popt = None
    perror = None
    pcov = None

    # set upper and lower bounds on a per-element basis
    if bounds is None:
        bounds = set_default_bounds(circuit, constants=constants)

    cg = CircuitGraph(circuit, constants)
    sumsq_errors = objective_function(cg, f, Z, weight_by_modulus=weight_by_modulus)
    if not global_opt:
        if opt_method == "minimize":
            if "options" not in kwargs:
                kwargs["options"] = _LBFGSB_OPTIONS
            bounds = [(lb, ub) for lb, ub in zip(*bounds)]
            result = minimize(
                sumsq_errors,
                initial_guess,
                bounds=bounds,
                **kwargs,
            )
            popt = result.x
            pcov = result.get("hess_inv", None)
            if (pcov is None) and ("hess" in result):
                pcov = inv(result.hess)
            try:
                pcov = pcov.todense()
            except AttributeError:
                pass
        else:
            if "maxfev" not in kwargs:
                kwargs["maxfev"] = 1e5
            if "ftol" not in kwargs:
                kwargs["ftol"] = 1e-13

            # weighting scheme for fitting
            if weight_by_modulus:
                abs_Z = np.abs(Z)
                kwargs["sigma"] = np.concatenate([abs_Z, abs_Z])

            popt, pcov = curve_fit(
                cg.compute_long,
                f,
                np.concatenate([Z.real, Z.imag]),
                p0=initial_guess,
                bounds=bounds,
                **kwargs,
            )

    else:
        if "seed" not in kwargs:
            kwargs["seed"] = 0

        if opt_method == "dual_annealing":
            if "local_search_options" not in kwargs:
                kwargs["local_search_options"] = _KWARGS
                kwargs["local_search_options"]["bounds"] = Bounds(
                    lb=bounds[0], ub=bounds[1]
                )

            bounds = (np.maximum(-1e9, bounds[0]), np.minimum(1e9, bounds[1]))

            results = dual_annealing(
                sumsq_errors,
                x0=initial_guess,
                bounds=np.asarray(bounds).T,
                **kwargs,
            )
            popt = results.x
            pcov = None
        else:
            if "minimizer_kwargs" not in kwargs:
                kwargs["minimizer_kwargs"] = _KWARGS

            results = basinhopping(
                sumsq_errors,
                x0=initial_guess,
                accept_test=BoundsCheck(*bounds),
                **kwargs,
            )

            popt = results.x
            pcov = results.get("lowest_optimization_result", {}).get("hess_inv", None)
            try:
                pcov = pcov.todense()
            except AttributeError:
                pass

    if (pcov is None) or np.any(np.diag(pcov) < 0):
        for m in ["central", "backward", "forward"]:
            hess = nd.Hessian(sumsq_errors, method=m)
            hmat = hess(popt)
            pcov = inv(hmat)
            if np.all(np.diag(pcov) >= 0):
                break
            pcov = None

    # Calculate one standard deviation error estimates for fit parameters,
    # defined as the square root of the diagonal of the covariance matrix.
    # https://stackoverflow.com/a/52275674/5144795
    if pcov is not None:
        perror = np.sqrt(np.diag(pcov))

    return (popt, perror) if not return_covariance else (popt, perror, pcov)


def extract_circuit_elements(circuit):
    """Extracts circuit elements from a circuit string.

    Parameters
    ----------
    circuit : str
        Circuit string.

    Returns
    -------
    extracted_elements : list
        list of extracted elements.

    """
    p_string = [x for x in circuit if x not in "p(),-"]
    extracted_elements = []
    current_element = []
    length = len(p_string)
    for i, char in enumerate(p_string):
        if char not in ints:
            current_element.append(char)
        else:
            # min to prevent looking ahead past end of list
            if p_string[min(i + 1, length - 1)] not in ints:
                current_element.append(char)
                extracted_elements.append("".join(current_element))
                current_element = []
            else:
                current_element.append(char)
    extracted_elements.append("".join(current_element))
    return extracted_elements


def calculateCircuitLength(circuit):
    """Calculates the number of elements in the circuit.

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
            num_params = circuit_elements[raw_element].num_params
            length += num_params
    return length


class CircuitGraph:
    _parallel_block_expression = re.compile(r"p\([^\(\)]*\)")
    _whitespce = re.compile(r"\s+")

    def __init__(self, circuit, constants=None):
        self.circuit = self._whitespce.sub("", circuit)

        self.parse_circuit()
        self.execution_order = list(nx.topological_sort(self.graph))
        self.constants = constants if constants is not None else dict()

    def parse_circuit(self):
        self.snum = 1
        self.pnum = 1

        parsing_circuit = self.circuit

        # determine all of the base elements, their functions and add them to the graph
        element_name = extract_circuit_elements(parsing_circuit)
        element_func = [
            circuit_elements[get_element_from_name(e)] for e in element_name
        ]
        self.graph = nx.DiGraph()
        for e, f in zip(element_name, element_func):
            self.graph.add_node(e, Z=f)

        # find unnested parallel blocks
        pblocks = self._parallel_block_expression.findall(parsing_circuit)
        while len(pblocks) > 0:
            # add parallel blocks to the graph unnesting each time around the loop
            for p in pblocks:
                pelem = p[2:-1].split(",")
                pnode = f"p{self.pnum}"
                self.pnum += 1
                self.graph.add_node(pnode, Z=circuit_elements["p"])
                for elem in pelem:
                    elem = self.add_series_elements(elem)
                    self.graph.add_edge(elem, pnode)
                parsing_circuit = parsing_circuit.replace(p, pnode)
            pblocks = self._parallel_block_expression.findall(parsing_circuit)

        # pick up any top line series connections
        self.add_series_elements(parsing_circuit)

        for layer, nodes in enumerate(nx.topological_generations(self.graph)):
            for n in nodes:
                self.graph.nodes[n]["layer"] = layer

    def add_series_elements(self, elem):
        selem = elem.split("-")
        if len(selem) > 1:
            node = f"s{self.snum}"
            self.snum += 1
            self.graph.add_node(node, Z=circuit_elements["s"])
            for n in selem:
                self.graph.add_edge(n, node)
            return node

        # if there isn't a series connection in elem just return it unchanged
        return selem[0]

    def visualize_graph(self, **kwargs):
        pos = nx.multipartite_layout(self.graph, subset_key="layer")
        nx.draw_networkx(self.graph, pos=pos, **kwargs)

    def compute(self, f, *parameters):
        node_results = {}
        pindex = 0
        for node in self.execution_order:
            Zfunc = self.graph.nodes[node]["Z"]
            plist = [node_results[pred] for pred in self.graph.predecessors(node)]
            if len(plist) < 1:
                n_params = Zfunc.num_params
                for j in range(n_params):
                    p_name = format_parameter_name(node, j, n_params)
                    if p_name in self.constants:
                        plist.append(self.constants[p_name])
                    else:
                        plist.append(parameters[pindex])
                        pindex += 1
                node_results[node] = Zfunc(plist, f)
            else:
                node_results[node] = Zfunc(plist)

        return np.squeeze(node_results[node])

    def __call__(self, f, *parameters):
        Z = self.compute(f, *parameters)
        return np.stack([Z.real, Z.imag])

    def compute_long(self, f, *parameters):
        Z = self.compute(f, *parameters)
        return np.concatenate([Z.real, Z.imag])

    def calculate_circuit_length(self):
        n_params = [
            getattr(Zfunc, "num_params", 0)
            for node, Zfunc in self.graph.nodes(data="Z")
        ]
        return np.sum(n_params)

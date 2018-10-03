import json
from .circuits import CustomCircuit
import numpy as np

def model_export(model, filepath):
    """Export the impedance model to a JSON file"""


    model_string = model.circuit

    model_name = model.name

    model_param_names = model.get_param_names()

    model_initial_guess = [(name, model.initial_guess[index])
                    for index, name in enumerate(model_param_names)]
    model_params = [(name, model.parameters_[index])
                    for index, name in enumerate(model_param_names)]


    if not model_name:
        model_name = "None"

    data_dict = {"Name":model_name,
                 "Circuit String":model_string,
                 "Initial Guess":model_initial_guess,
                 "Parameters":model_params
    }

    print("Exporting the following model to destination %s"%filepath)
    print(model)

    destination_object = open(filepath, 'w')

    json.dump(data_dict, destination_object)


def model_import(filepath, as_initial_guess = False):
    """ Imports parameters of a model from JSON

    Parameters
    ---------

    as_initial_guess: bool
        If True, imports the fitted parameters from json as an unfitted model
        otherwise imports the data as a fitted model object

    Returns
    ----------
    circuit_model: CustomCircuit
        Circuit model object


    """

    json_data_file = open(filepath, 'r')


    json_data = json.load(json_data_file)




    circuit_name = json_data["Name"]

    if circuit_name == 'None':
        circuit_name = None

    circuit_string = json_data["Circuit String"]
    circuit_param_list = json_data["Parameters"]
    circuit_ig_list = json_data["Initial Guess"]

    circuit_params = [item[1] for item in circuit_param_list]
    circuit_initial_guess = [item[1] for item in circuit_ig_list]
    print(circuit_initial_guess)

    # If this is being loaded as an initial guess, load the fitted circuit parameters as an initial guess
    if as_initial_guess:

        circuit_model = CustomCircuit(initial_guess=circuit_params, circuit=circuit_string, name=circuit_name)

    else:

        circuit_model = CustomCircuit(initial_guess=circuit_initial_guess, circuit=circuit_string, name=circuit_name)
        circuit_model.parameters_ = np.array(circuit_params)


    print("Imported model from %s with the following circuit parameters"%filepath)
    print(circuit_model)

    return circuit_model


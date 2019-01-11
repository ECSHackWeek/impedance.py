import json
from .circuits import CustomCircuit
import numpy as np


def model_export(model, filepath):
    """ Exports a model to JSON

    Parameters
    ---------

    model: CustomCircuit
        Circuit model object

    filepath: Path String
        Destination for exporting model object


    """

    model_string = model.circuit
    model_name = model.name

    initial_guess = model.initial_guess

    if model._is_fit():
        parameters_ = list(model.parameters_)
        model_conf_ = list(model.conf_)

        data_dict = {"Name": model_name,
                     "Circuit String": model_string,
                     "Initial Guess": initial_guess,
                     "Fit": True,
                     "Parameters": parameters_,
                     "Confidence": model_conf_,
                     }
    else:
        data_dict = {"Name": model_name,
                     "Circuit String": model_string,
                     "Initial Guess": initial_guess,
                     "Fit": False}

    with open(filepath, 'w') as f:
        json.dump(data_dict, f)


def model_import(filepath):
    """ Imports a model from JSON

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

    model_name = json_data["Name"]
    if model_name == 'None':
        model_name = None

    model_string = json_data["Circuit String"]
    model_initial_guess = json_data["Initial Guess"]

    circuit_model = CustomCircuit(initial_guess=model_initial_guess,
                                  circuit=model_string,
                                  name=model_name)

    if json_data["Fit"]:
        circuit_model.parameters_ = np.array(json_data["Parameters"])
        circuit_model.conf_ = np.array(json_data["Confidence"])

    return circuit_model

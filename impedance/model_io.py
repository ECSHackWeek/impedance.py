import json
from .circuits import CustomCircuit

def model_export(model, filepath):
    """Export the impedance model to a JSON file"""


    model_string = model.circuit

    model_param_names = model.get_names()

    model_params = [(name, model.parameters_[index])
                    for index, name in enumerate(model_param_names)]


    print("Exporting the following model to destination")

    destination_object = open(filepath, 'w')

    json.dump([model_string, model_params], destination_object)


def model_import(filepath):

    """Import the file from JSON and construct a circuit element from it"""

    json_data_file = open(filepath, 'r')


    json_data = json.load(json_data_file)

    circuit_string = json_data[0]

    circuit_param_list = json_data[1]

    circuit_params = [item[1] for item in circuit_param_list]

    circuit_model = CustomCircuit(initial_guess=circuit_params, circuit=circuit_string)

    "Imported model with the following circuit parameters"
    print(circuit_model)

    return circuit_model


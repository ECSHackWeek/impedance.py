import json


def model_export(model, filepath):
    """Export the impedance model to a .py file"""


    model_string = model.circuit

    model_param_names = model.get_names()

    model_params = [(name, model.parameters_[index])
                    for index, name in enumerate(model_param_names)]


    print("Exporting the following model to destination")

    destination_object = open(filepath, 'w')

    json.dump([model_string, model_params], destination_object)


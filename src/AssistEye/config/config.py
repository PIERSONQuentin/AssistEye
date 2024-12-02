"""
Config Module

This module provides functionalities for loading configuration and selecting devices.

Available functions:
- load_config(config_path): Load configuration from a YAML file.
- select_device(user_input): Select the device to use for computation.
"""

import os
import sys
import yaml
import torch

config_data = {}
device = None
config_path = None

def load_config(path_to_config):
    """
    Load configuration from a YAML file.

    Args:
        config_path (str): The path to the YAML configuration file.

    Returns:
        dict: The configuration data loaded from the file.
    """
    global config_data, config_path
    with open(path_to_config, 'r') as file:
        config_data = yaml.safe_load(file)
        print("AssistEye config loaded successfully.")
    # Add the path to the AssistEye module
    sys.path.append(os.path.abspath(config_data['general']['path'] + '/src'))
    config_path = path_to_config
    return config_data

def select_device(user_input):
    """
    Select the device to use for computation.

    Args:
        user_input (str): The user's choice of device.

    Returns:
        str: The name of the selected device.
    """
    global device
    if user_input == "gpu":
        if torch.cuda.is_available():
            device = "cuda"
        elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
            device = "mps"
        else:
            print("Aucun GPU disponible, utilisation du CPU.")
            device = "cpu"
    elif user_input == "cpu":
        device = "cpu"
    else:
        if torch.cuda.is_available():
            device = "cuda"
        elif torch.backends.mps.is_available() and torch.backends.mps.is_built():
            device = "mps"
        else:
            device = "cpu"
    return device

# def update_config_param(section, param_name, param_value):
    """
    Update a parameter in the config.yaml file.

    Args:
        section (str): The section where the parameter is located.
        param_name (str): The name of the parameter to update.
        param_value: The new value of the parameter.

    Returns:
        str: A message indicating the success or failure of the update.
    """
    global config_data, config_path

    # Récupérer la langue actuelle
    language = config_data['general']['language']
    print("Current language:", language)
    responses = config_data.get('translations', {}).get(language, {}).get('responses', {})
    # Si les traductions ne sont pas disponibles, utiliser la section 'responses' par défaut
    if not responses:
        responses = config_data.get('responses', {})

    if not config_data or not config_path:
        error_message = responses.get('config_update_error', "Erreur lors de la mise à jour du paramètre '{param}'.")
        error_message = error_message.format(param=param_name)
        print(error_message)
        return error_message

    if section in config_data:
        config_data[section][param_name] = param_value
        with open(config_path, 'w') as file:
            yaml.dump(config_data, file)
        success_message = responses.get('config_update_success', "Le paramètre '{param}' a été mis à jour avec succès.")
        success_message = success_message.format(param=param_name)
        print(success_message)
        return success_message
    else:
        error_message = responses.get('config_update_error', "Erreur lors de la mise à jour du paramètre '{param}'.")
        error_message = error_message.format(param=param_name)
        print(error_message)
        return error_message
    



def update_config_param(section, param_name, param_value):
    """
    Update a parameter in the config.yaml file directly by editing the relevant line.

    Args:
        section (str): The section where the parameter is located.
        param_name (str): The name of the parameter to update.
        param_value: The new value of the parameter.

    Returns:
        str: A message indicating the success or failure of the update.
    """
    global config_path

    try:
        # Read the file line by line
        with open(config_path, 'r') as file:
            lines = file.readlines()

        # Variables to track the current section and update status
        current_section = None
        updated = False

        # Process each line
        for i, line in enumerate(lines):
            # Detect section headers
            if line.startswith(section + ':'):
                current_section = section

            # Update the parameter if we're in the right section
            if current_section == section and line.strip().startswith(f'{param_name}:'):
                lines[i] = f'  {param_name}: {param_value}\n'
                updated = True
                break

        if not updated:
            return "Parameter not found in configuration."

        # Write back the updated file
        with open(config_path, 'w') as file:
            file.writelines(lines)

        return f"Parameter '{param_name}' updated successfully."

    except Exception as e:
        return f"Error updating configuration: {str(e)}"


# Charger automatiquement la configuration lors de l'importation du module
# Verifier si le fichier custom.yaml existe
custom_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../config/custom.yaml'))
default_config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../config/default.yaml'))
if os.path.exists(custom_config_path):
    load_config(custom_config_path)
else:
    load_config(default_config_path)

select_device(config_data['general']['device'])




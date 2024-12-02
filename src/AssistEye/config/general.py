"""
General configuration module for AssistEye.

This module contains methods for updating general configuration settings.
"""

# use the update_config_param method to update the configuration settings
# si un paramètre de configuration mis à jour alors on copie la config par défaut sous 
# le nom de custom.yaml et on met à jour le paramètre dans ce fichier
# si ce fichier existe alors on le charge au lieu de charger le fichier par défaut

import os
global config_data

# todo : placeholder 
def select_configuration_file(name):
    """
    Select the configuration file to use.

    Args:
        name (str): The name of the configuration file to use.

    Returns:
        str: The path to the selected configuration file.
    """
    #config_path = f"config/{name}.yaml"
    config_path = os.path.join(os.path.dirname(__file__), f"../../../config/{name}.yaml")

    # ensure the configuration file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.") 
    return config_path


def update_language(language):
    """
    Update the language setting in the configuration.

    Args:
        language (str): The language to set in the configuration.

    Returns:
        None
    """
    global config_data
    config_data['general']['language'] = language

def update_detection_model(model_name):
    """
    Update the object detection model setting in the configuration.

    Args:
        model_name (str): The name of the object detection model to set in the configuration.

    Returns:
        None
    """
    global config_data
    config_data['general']['detection_model_name'] = model_name

def update_text_model(model_name):
    """
    Update the text detection model setting in the configuration.

    Args:
        model_name (str): The name of the text detection model to set in the configuration.

    Returns:
        None
    """
    global config_data
    config_data['general']['text_model_name'] = model_name

def update_depth_model(model_name):
    """
    Update the depth estimation model setting in the configuration.

    Args:
        model_name (str): The name of the depth estimation model to set in the configuration.

    Returns:
        None
    """
    global config_data
    config_data['general']['depth_model_name'] = model_name

def update_translations(translations_dict):
    """
    Update the translations dictionary setting in the configuration.

    Args:
        translations_dict (dict): The translations dictionary to set in the configuration.

    Returns:
        None
    """
    global config_data
    config_data['translations'] = translations_dict


def get_translations():
    """
    Get the translations dictionary from the default configuration.

    Returns:
        dict: The translations dictionary from the configuration.
    """
    global config_data
    return config_data['translations']
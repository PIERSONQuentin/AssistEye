"""
Translation Module

This module provides functionalities for translating object labels and responses.

Available functions:
- set_language(lang): Change the translation language.
- translate_label(label): Translate an object label.
- get_response(key, **kwargs): Get a translated response.
"""

translations = {}
current_language = "fr"

def translation_init(translations_dict, default_language="fr"):
    """
    Initialize the translator with available translations.

    Args:
        translations_dict (dict): Dictionary containing translations.
        default_language (str): Default language for translations.
    """
    global translations, current_language
    translations = translations_dict
    current_language = default_language

def set_language(lang):
    """
    Change the translation language.

    Args:
        lang (str): The language code to use.
    """
    global current_language
    if lang in translations:
        current_language = lang
        print(f"Langue définie sur : {lang}")
    else:
        print(f"Langue '{lang}' non disponible. Langue par défaut : 'fr'.")

def translate_label(label):
    """
    Translate an object label.

    Args:
        label (str): The label to translate.

    Returns:
        str: The translated label.
    """
    return translations[current_language]["labels"].get(label, label)

def get_response(key, **kwargs):
    """
    Get a translated response.

    Args:
        key (str): The key of the response to get.
        **kwargs: Arguments to format in the response.

    Returns:
        str: The translated response.
    """
    response_template = translations[current_language]["responses"][key]
    return response_template.format(**kwargs)
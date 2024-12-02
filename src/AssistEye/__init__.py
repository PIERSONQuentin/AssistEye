"""
AssistEye Module

This module provides functionalities for object detection, depth estimation,
translation, voice assistance, and visualization.
"""

# supress warnings
import warnings
warnings.filterwarnings("ignore")

# Import sub-modules
from . import config
from .detection import objectDetection
from .detection import textDetection
from . import depth, translation, voiceAssistant, visualization

# Access configuration data and device
config_data = config.config_data
device = config.device


objectDetection.initialization(model_name=config_data['general']['detection_model_name'], device_name=device)
textDetection.initialization(model_name=config_data['general']['text_model_name'], device_name=device)
depth.depth_init(model_name=config_data['general']['depth_model_name'],  device_name=device)
translation.translation_init(translations_dict=config_data['translations'], default_language=config_data['general']['language'])
voiceAssistant.voiceAssistant_init(translator_instance=translation)
visualization.visualization_init(config_dict=config_data)

print("AssistEye module loaded successfully.")

# Declare sub-modules in __all__
__all__ = ['config', 'detection', 'depth', 'translation', 'voiceAssistant', 'visualization']
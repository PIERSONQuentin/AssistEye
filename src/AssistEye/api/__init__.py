"""
API Module 

This module provides functionalities for the API of the AssistEye system.
"""

from .api import api_init, run_api, detect_objects, detect_text

__all__ = ['api_init', 'run_api', 'detect_objects', 'detect_text']
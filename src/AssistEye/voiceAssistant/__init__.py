"""
Voice Assistant Module

This module provides functionalities for speech synthesis and recognition.
"""

from .voiceAssistant import voiceAssistant_init, respond, listen, process_command

__all__ = ['voiceAssistant_init', 'respond', 'listen', 'process_command']
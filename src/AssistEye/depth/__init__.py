"""
Depth Module

This module provides functionalities for depth estimation using the MiDaS model.
"""

from .depth import depth_init, estimate_depth, convert_depth_to_distance, configure_depth_map

__all__ = ['depth_init', 'estimate_depth', 'convert_depth_to_distance', 'configure_depth_map']
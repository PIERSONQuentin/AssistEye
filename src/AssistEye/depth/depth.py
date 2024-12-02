"""
Depth Module

This module provides functionalities for depth estimation using the MiDaS model.

Available functions:
- estimate_depth(image): Estimate the depth of an image.
- convert_depth_to_distance(mean_depth, scale_factor=0.5): Convert a mean depth value to distance.
- configure_depth_map(frame, depth_model_instance, display_mode="rgb"): Configure the depth map and display it in RGB or grayscale.
"""

import torch
from torchvision.transforms import Compose, Resize, ToTensor, Normalize
from torchvision.transforms.functional import InterpolationMode
import yaml
import torch
import cv2
import numpy as np
from PIL import Image
from AssistEye import config # Import the configuration module

device = None  # Will be set in the initialize function
model = None
transform = None
unit_system = "steps" # Default unit system for distance

def depth_init(model_name, device_name):
    """
    Initialize the MiDaS model for depth estimation.

    Args:
        device_name (str): The device to use for computations ("cpu", "cuda", "mps").
    """
    global device, model, transform
    device = device_name
    model = torch.hub.load("intel-isl/MiDaS", model_name).to(device)
    model.eval()
    transform = Compose([
        Resize((256, 256), interpolation=InterpolationMode.BILINEAR),
        ToTensor(),
        Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # retrieve the unit system from the configuration file
    unit_system = config.config_data['general']['unit_system']

def estimate_depth(image):
    """
    Estimate the depth of an image.

    Args:
        image (PIL.Image): The image for which to estimate depth.

    Returns:
        numpy.ndarray: The estimated depth map.
    """
    input_batch = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        depth_map = model(input_batch).squeeze().cpu().numpy()
    return depth_map

    

    
def convert_depth_to_distance(mean_depth, scale_factor=0.5, min_distance=0.1, max_distance=100):
    """
    Convert a mean depth value to distance in the desired unit system.

    Args:
        mean_depth (float): The mean depth value.
        scale_factor (float): The calibration factor for distance.
        min_distance (float): Minimum valid distance (in meters).
        max_distance (float): Maximum valid distance (in meters).

    Returns:
        float or str: The estimated distance in the specified unit, or a string indicating 'too_close' or 'too_far'.
    """
    if mean_depth <= 0:
        return 'too_close'

    # Convert depth to distance
    distance_meters = scale_factor / (mean_depth ** 1.1)

    # Check if distance is within valid range
    if distance_meters < min_distance:
        return 'too_close'
    elif distance_meters > max_distance:
        return 'too_far'

    # Convert to desired unit
    unit_system = config.config_data['general']['unit_system']
    if unit_system == 'meters':
        return distance_meters
    elif unit_system == 'feet':
        return distance_meters * 3.28084  # 1 mètre = 3.28084 pieds
    elif unit_system == 'steps':
        average_step_length = 0.762  # Longueur moyenne d'un pas en mètres
        return distance_meters / average_step_length
    else:
        # Par défaut, retourner la distance en mètres si l'unité n'est pas reconnue
        return distance_meters



def configure_depth_map(frame, depth_model_instance, display_mode="rgb"):
    """
    Configure the depth map and display it in RGB or grayscale.

    Args:
        frame (numpy.ndarray): The input frame from the webcam.
        depth_model_instance: The depth model instance.
        display_mode (str): The display mode ("rgb" or "grayscale").

    Returns:
        tuple: The normalized depth map and the processed image.
    """
    if display_mode == "rgb":
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    else:
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    
    pil_image = Image.fromarray(image)
    depth_map = depth_model_instance.estimate_depth(pil_image)
    depth_map = cv2.resize(depth_map, (frame.shape[1], frame.shape[0]))
    depth_map_normalized = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())
    
    return depth_map_normalized, image
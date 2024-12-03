"""
Text Detection Module

This module provides functionalities for text detection using the pytesseract model.

Available functions:
- initialization(model_name, device_name): Initialize the pytesseract text detection model.
- detect(frame): Perform text detection on an image.
- process_results(results): Process text detection results.
- run_inference(path, annotations): Run inference on an image or video file.
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
from AssistEye import config

model = None  # Will be initialized in the initialize function

def initialization(model_name, device_name):
    """
    Initialize the Tesseract OCR model.
    """
    # Verify if Tesseract is properly configured
    if not pytesseract.get_tesseract_version():
        raise RuntimeError("Tesseract is not configured correctly or not installed.")
        
    # Set the global model
    global model
    model = pytesseract


def detect(frame):
    """
    Perform text detection using Tesseract with additional preprocessing.

    Args:
        frame (numpy.ndarray): The image on which to perform text detection.

    Returns:
        dict: A dictionary containing the detection results (compatible with process_results).
    """
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Try different preprocessing steps
    preprocess_methods = [
        lambda img: cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[1],  # Simple binary threshold
        lambda img: cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2),  # Adaptive threshold
        lambda img: cv2.GaussianBlur(img, (5, 5), 0),  # Gaussian blur
        lambda img: cv2.bitwise_not(img),  # Invert the image
    ]

    best_results = None
    max_confidence = -1

    for preprocess in preprocess_methods:
        # Apply preprocessing
        processed_image = preprocess(gray)

        # Perform OCR
        results = pytesseract.image_to_data(processed_image, output_type=pytesseract.Output.DICT)

        # Check confidence level to select the best result
        conf_values = [int(conf) for conf in results['conf'] if conf != '-1']
        avg_confidence = sum(conf_values) / len(conf_values) if conf_values else 0

        if avg_confidence > max_confidence:
            max_confidence = avg_confidence
            best_results = results

    return best_results

    



def process_results(results):
    """
    Process text detection results.

    Args:
        results (dict): The detection results.
    
    Returns:
        tuple: A tuple containing the detected text and their positions.
    """
    detected_texts = []
    text_positions = []

    n_boxes = len(results['level'])
    for i in range(n_boxes):
        if int(results['conf'][i]) > 0:
            text = results['text'][i]
            x = results['left'][i]
            y = results['top'][i]
            w = results['width'][i]
            h = results['height'][i]
            detected_texts.append(text)
            text_positions.append((x, y, w, h))

    return detected_texts, text_positions

# def run_inference(path, annotations):
    """
    Run inference on an image or video file or array with specified annotations.

    Args:
        path (str): The path to the image or video file.
        annotations (dict): Dictionary specifying which annotations to include.
    """
    # Load the image 
    frame = cv2.imread(path)
    if frame is None:
        print("Error loading image")
        return

    # Detect text in the image
    results = detect(frame)

    # Process the detection results
    detected_texts, text_positions = process_results(results)

    # Annotate the image if needed
    if annotations.get('class', False):
        for (text, (x, y, w, h)) in zip(detected_texts, text_positions):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if annotations.get('confidence', False):
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Convert image from BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the annotated image using plt
    import matplotlib.pyplot as plt
    plt.imshow(frame_rgb)
    plt.title("Text Detection")
    plt.axis('off')  # Hide axis
    plt.show()

def run_inference(path_or_array, annotations):
    """
    Run inference on an image or video file or array with specified annotations.

    Args:
        path_or_array (str or numpy.ndarray): The path to the image or video file, or the image array.
        annotations (dict): Dictionary specifying which annotations to include.
    """
    # Check if input is a path or an image array
    if isinstance(path_or_array, str):
        # Load the image from the path
        frame = cv2.imread(path_or_array)
        if frame is None:
            print("Error loading image")
            return
    elif isinstance(path_or_array, np.ndarray):
        # Use the provided image array
        frame = path_or_array
    else:
        print("Invalid input type. Provide a file path or an image array.")
        return

    # Detect text in the image
    results = detect(frame)

    # Process the detection results
    detected_texts, text_positions = process_results(results)

    # Annotate the image if needed
    if annotations.get('class', False):
        for (text, (x, y, w, h)) in zip(detected_texts, text_positions):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if annotations.get('confidence', False):
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Convert image from BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the annotated image using plt
    import matplotlib.pyplot as plt
    plt.imshow(frame_rgb)
    plt.title("Text Detection")
    plt.axis('off')  # Hide axis
    plt.show()
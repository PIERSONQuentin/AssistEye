"""
API for AssistEye

This module provides functionalities for the API of the AssistEye system.

Available functions:
- api_init(): Initialize the API.
- run_api(): Run the API.
"""

import io
import numpy as np
from PIL import Image

def api_init():
    """
    Initialize the API.
    """
    from AssistEye.config import config
    from AssistEye.detection import objectDetection, textDetection, depthEstimation

    # Access configuration data and device
    config_data = config.config_data
    device = config.device

    objectDetection.initialization(model_name=config_data['general']['detection_model_name'], device_name=device)
    textDetection.initialization(model_name=config_data['general']['text_model_name'], device_name=device)
    depthEstimation.initialization(model_name=config_data['general']['depth_model_name'],  device_name=device)


def run_api(): 
    """
    Run the API.
    """
    from flask import Flask, request, jsonify
    from AssistEye.detection.objectDetection import detect, process_results
    from AssistEye.detection.textDetection import detect_text, process_text_results

    app = Flask(__name__)

    @app.route('/detect_objects', methods=['POST'])
    def detect_objects():
        """
        Perform object detection on an image.
        """
        if request.method == 'POST':
            # Get the image from the request
            image = request.files['image'].read()
            image = Image.open(io.BytesIO(image))
            image = np.array(image)

            # Perform object detection
            results = detect(image)
            object_counts, distances = process_results(results)

            return jsonify(object_counts=object_counts, distances=distances)

    @app.route('/detect_text', methods=['POST'])
    def detect_text():
        """
        Perform text detection on an image.
        """
        if request.method == 'POST':
            # Get the image from the request
            image = request.files['image'].read()
            image = Image.open(io.BytesIO(image))
            image = np.array(image)

            # Perform text detection
            results = detect_text(image)
            detected_texts, text_positions = process_text_results(results)

            return jsonify(detected_texts=detected_texts, text_positions=text_positions)

    app.run(host='', port=5000)
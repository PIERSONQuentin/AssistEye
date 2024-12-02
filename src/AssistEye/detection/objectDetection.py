"""
Object Detection Module

This module provides functionalities for object detection using YOLO models.

Available functions:
- initialization(model_name, device_name): Initialize the YOLO detection model.
- detect(frame): Perform object detection on an image.
- process_results(results, depth_map_normalized, depth_model): Process detection results to extract object counts and distances.
- run_inference(path, annotations): Run inference on an image or video file with specified annotations.
"""

from ultralytics import YOLO
import numpy as np
import cv2
from PIL import Image
from AssistEye import config, depth, visualization

model = None  # Will be initialized in the initialize function

def initialization(model_name, device_name):
    """
    Initialize the YOLO detection model.

    Args:
        model_name (str): The name of the YOLO model to use.
        device (str): The device to use for computations ("cpu", "cuda", "mps").
    """
    print("Initializing object detection model...")
    print(f"Model: {model_name}, Device: {device_name}")
    global model
    model = YOLO(model_name).to(device_name)

def detect(frame):
    """
    Perform object detection on an image.

    Args:
        frame (numpy.ndarray): The image on which to perform detection.

    Returns:
        list: The detection results.
    """
    return model(frame, conf=0.4)


# def process_results(results, depth_map_normalized):
    """
    Process detection results to extract object counts and distances.

    Args:
        results (list): The detection results.
        depth_map_normalized (numpy.ndarray): The normalized depth map.

    Returns:
        tuple: A tuple containing object counts and distances.
    """
    object_counts = {}
    distances = {}

    for result in results:
        for detection in result.boxes:
            bbox = detection.xyxy[0]
            x1, y1, x2, y2 = map(int, bbox[:4].tolist())
            depth_roi = depth_map_normalized[y1:y2, x1:x2]
            mean_depth = np.median(depth_roi)
            distance = depth.convert_depth_to_distance(mean_depth)

            class_id = int(detection.cls[0].item()) if hasattr(detection, 'cls') else None
            class_name = model.names[class_id] if class_id is not None and class_id in model.names else "Objet"

            object_counts[class_name] = object_counts.get(class_name, 0) + 1
            distances.setdefault(class_name, []).append(distance)

    return object_counts, distances

# def process_results(results, depth_map_normalized=None, return_positions=False):
    """
    Process detection results to extract object counts and optionally distances and positions.

    Args:
        results (list): The detection results.
        depth_map_normalized (numpy.ndarray, optional): The normalized depth map.
        return_positions (bool, optional): If True, include positions of detected objects in the return value.

    Returns:
        tuple: A tuple containing object counts, distances, and optionally positions.
               If depth_map_normalized is not provided, distances will be an empty dictionary.
               If return_positions is False, positions will not be included in the return value.
    """
    object_counts = {}
    distances = {}
    positions = {} if return_positions else None

    for result in results:
        for detection in result.boxes:
            bbox = detection.xyxy[0]
            x1, y1, x2, y2 = map(int, bbox[:4].tolist())

            # Calculate distances only if depth_map_normalized is provided
            if depth_map_normalized is not None:
                depth_roi = depth_map_normalized[y1:y2, x1:x2]
                mean_depth = np.median(depth_roi)
                distance = depth.convert_depth_to_distance(mean_depth)
            else:
                distance = None

            class_id = int(detection.cls[0].item()) if hasattr(detection, 'cls') else None
            class_name = model.names[class_id] if class_id is not None and class_id in model.names else "Objet"

            object_counts[class_name] = object_counts.get(class_name, 0) + 1

            if distance is not None:
                distances.setdefault(class_name, []).append(distance)

            if return_positions:
                bbox_coords = (x1, y1, x2, y2)
                positions.setdefault(class_name, []).append(bbox_coords)

    if return_positions:
        return object_counts, distances, positions
    else:
        return object_counts, distances

def process_results(results, depth_map_normalized=None, return_positions=False):
    """
    Process detection results to extract object counts, distances, and optionally positions.

    Args:
        results (list): The detection results.
        depth_map_normalized (numpy.ndarray, optional): The normalized depth map. If not provided, distances will be empty.
        return_positions (bool, optional): Whether to include positions in the return value.

    Returns:
        tuple: A tuple containing object counts, distances, and optionally positions.
    """
    object_counts = {}
    distances = {}
    positions = {} if return_positions else None

    for result in results:
        for detection in result.boxes:
            bbox = detection.xyxy[0]
            x1, y1, x2, y2 = map(int, bbox[:4].tolist())

            # Calculate distances only if depth_map_normalized is provided
            if depth_map_normalized is not None:
                depth_roi = depth_map_normalized[y1:y2, x1:x2]
                mean_depth = np.median(depth_roi)
                distance = depth.convert_depth_to_distance(mean_depth)
            else:
                distance = None

            class_id = int(detection.cls[0].item()) if hasattr(detection, 'cls') else None
            class_name = model.names[class_id] if class_id is not None and class_id in model.names else "Objet"

            object_counts[class_name] = object_counts.get(class_name, 0) + 1

            if distance is not None:
                distances.setdefault(class_name, []).append(distance)

            if return_positions:
                bbox_coords = (x1, y1, x2, y2)
                positions.setdefault(class_name, []).append(bbox_coords)

    if return_positions:
        return object_counts, distances, positions
    else:
        return object_counts, distances



def crop_objects(image, positions):
    """
    Crop regions of interest from the image based on object positions.

    Args:
        image (numpy.ndarray): Original image.
        positions (dict): Dictionary containing class names as keys and lists of bounding boxes as values.

    Returns:
        dict: Cropped images for each class and bounding box.
    """
    cropped_images = {}
    for class_name, bboxes in positions.items():
        cropped_images[class_name] = []
        for bbox in bboxes:
            x1, y1, x2, y2 = bbox
            cropped_region = image[y1:y2, x1:x2]
            cropped_images[class_name].append(cropped_region)
    return cropped_images


def run_inference(path, annotations):
    """
    Run inference on an image or video file with specified annotations.

    Args:
        path (str): The path to the image or video file.
        annotations (dict): Dictionary specifying which annotations to include.
    """

    if path.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Process image
        image = Image.open(path)
        depth_map = depth.estimate_depth(image)
        depth_map_normalized = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())

        # Convert the image to a NumPy array
        image_np = np.array(image)

        results = detect(image_np)
        object_counts, distances = process_results(results, depth_map_normalized)

        # Pass the image and depth map to draw_bounding_boxes with display_in_notebook=True
        visualization.draw_bounding_boxes(image_np, model, results, annotations, depth_map_normalized, display_in_notebook=True)
    else:
        # Process video
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            print("Error: Unable to open the video file")
            return

        window_name = 'Video'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Create a resizable window

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                depth_map_normalized, processed_image = depth.configure_depth_map(frame, depth, display_mode="rgb")
                results = detect(frame)
                object_counts, distances = process_results(results, depth_map_normalized)

                # Draw bounding boxes on the video frame and get the annotated frame
                annotated_frame = visualization.draw_bounding_boxes(frame, model, results, annotations, depth_map_normalized, display_in_notebook=False)

                # Display the annotated frame
                cv2.imshow(window_name, annotated_frame)

                # Check if the window was closed
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    break

                # Optional: You can still allow exiting with the 'q' key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except KeyboardInterrupt:
            print("\nUser interruption. Closing the program.")
        finally:
            cap.release()
            cv2.destroyAllWindows()

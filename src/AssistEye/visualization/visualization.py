"""
Visualization Module

This module provides functionalities for visualizing detection results.

Available functions:
- draw_bounding_boxes(image, results, annotations): Draw bounding boxes on the image or video frame with specified annotations.
"""

import cv2

import matplotlib.pyplot as plt
import numpy as np
from AssistEye import depth


config = {}

def initialization(config_dict):
    """
    Initialize the visualization module with configuration.

    Args:
        config_dict (dict): Configuration dictionary.
    """
    global config
    config = config_dict

'''
def draw_bounding_boxes(image, model, results, annotations, depth_map_normalized):
    """
    Draw bounding boxes on the image or video frame with specified annotations.

    Args:
        image (numpy.ndarray): The image or video frame.
        model: The detection model used.
        results (list): The detection results.
        annotations (dict): Dictionary specifying which annotations to include.
        depth_map_normalized (numpy.ndarray): The normalized depth map.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Récupérer la langue actuelle depuis la configuration
    current_language = config['general']['language']
    translations = config['translations'][current_language]['responses']

    # Convertir l'image de RGB à BGR pour les opérations OpenCV
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    for result in results:
        for detection in result.boxes:
            bbox = detection.xyxy[0]
            x1, y1, x2, y2 = map(int, bbox[:4].tolist())
            # S'assurer que les coordonnées sont dans les limites de l'image
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(image_bgr.shape[1], x2)
            y2 = min(image_bgr.shape[0], y2)

            # Calculer la distance
            depth_roi = depth_map_normalized[y1:y2, x1:x2]
            mean_depth = np.median(depth_roi)

            # Vérifier si mean_depth est un nombre valide
            if np.isnan(mean_depth) or mean_depth <= 0:
                distance = 'too_close'
            else:
                distance = depth.convert_depth_to_distance(mean_depth)

            class_id = int(detection.cls[0].item()) if hasattr(detection, 'cls') else None
            class_name = model.names[class_id] if class_id is not None and class_id in model.names else "Objet"
            confidence = detection.conf[0].item() if hasattr(detection, 'conf') else None

            # Construire le label en fonction des annotations
            label_lines = []
            if annotations.get('class') and class_name:
                label_lines.append(class_name)
            if annotations.get('confidence') and confidence is not None:
                label_lines.append(f'{confidence:.2f}')

            if annotations.get('distance'):
                if isinstance(distance, float):
                    # Format de la distance en fonction du système d'unités
                    unit_system = config['general']['unit_system']
                    if unit_system == 'meters':
                        distance_str = f'{distance:.2f} m'
                    elif unit_system == 'feet':
                        distance_str = f'{distance:.2f} ft'
                    elif unit_system == 'steps':
                        distance_str = f'{distance:.2f} steps'
                    else:
                        distance_str = f'{distance:.2f} m'  # Par défaut en mètres
                elif distance == 'too_close':
                    distance_str = translations.get('too_close', 'Trop proche')
                elif distance == 'too_far':
                    distance_str = translations.get('too_far', 'Hors de portée')
                else:
                    distance_str = translations.get('unknown_distance', 'Distance inconnue')
                label_lines.append(distance_str)

            # Dessiner la boîte englobante
            cv2.rectangle(image_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Procéder si des labels doivent être affichés
            if label_lines:
                # Calculer la hauteur totale du label
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                font_thickness = 1
                line_height = cv2.getTextSize('Tg', font, font_scale, font_thickness)[0][1] + 5  # Hauteur approximative de ligne

                total_label_height = line_height * len(label_lines)

                # Position de départ pour les labels
                label_x = x1
                label_y = y1 - total_label_height - 10  # 10 pixels au-dessus de la boîte

                # Ajuster si label_y est hors de l'image
                if label_y < 0:
                    label_y = y1 + 10  # Placer en dessous de la boîte

                # Dessiner le rectangle de fond pour les labels
                max_label_width = max([cv2.getTextSize(line, font, font_scale, font_thickness)[0][0] for line in label_lines]) + 10
                cv2.rectangle(image_bgr, (label_x, label_y), (label_x + max_label_width, label_y + total_label_height), (0, 255, 0), -1)

                # Ajouter chaque ligne de texte
                for i, line in enumerate(label_lines):
                    text_x = label_x + 5  # Padding à l'intérieur du rectangle
                    text_y = label_y + (i + 1) * line_height - 5  # Ajuster pour la ligne de base
                    cv2.putText(image_bgr, line, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness)

    # Convertir l'image en RGB pour l'affichage avec matplotlib
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # Afficher l'image annotée dans le notebook
    plt.figure(figsize=(10, 8))
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.show()
'''

def draw_bounding_boxes(image, model, results, annotations, depth_map_normalized, display_in_notebook=False):
    """
    Draw bounding boxes on the image or video frame with specified annotations.

    Args:
        image (numpy.ndarray): The image or video frame.
        model: The detection model used.
        results (list): The detection results.
        annotations (dict): Dictionary specifying which annotations to include.
        depth_map_normalized (numpy.ndarray): The normalized depth map.
        display_in_notebook (bool): If True, display the image in the notebook using matplotlib.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Récupérer la langue actuelle depuis la configuration
    current_language = config['general']['language']
    translations = config['translations'][current_language]['responses']

    if display_in_notebook:
        # Convertir l'image de RGB à BGR pour les opérations OpenCV
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    else:
        # Si l'image est déjà en BGR (vidéo), on l'utilise directement
        image_bgr = image

    for result in results:
        for detection in result.boxes:
            bbox = detection.xyxy[0]
            x1, y1, x2, y2 = map(int, bbox[:4].tolist())
            # S'assurer que les coordonnées sont dans les limites de l'image
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(image_bgr.shape[1], x2)
            y2 = min(image_bgr.shape[0], y2)

            # Calculer la distance
            depth_roi = depth_map_normalized[y1:y2, x1:x2]
            mean_depth = np.median(depth_roi)

            # Vérifier si mean_depth est un nombre valide
            if np.isnan(mean_depth) or mean_depth <= 0:
                distance = 'too_close'
            else:
                distance = depth.convert_depth_to_distance(mean_depth)

            class_id = int(detection.cls[0].item()) if hasattr(detection, 'cls') else None
            class_name = model.names[class_id] if class_id is not None and class_id in model.names else "Objet"
            confidence = detection.conf[0].item() if hasattr(detection, 'conf') else None

            # Construire le label en fonction des annotations
            label_lines = []
            if annotations.get('class') and class_name:
                label_lines.append(class_name)
            if annotations.get('confidence') and confidence is not None:
                label_lines.append(f'{confidence:.2f}')

            if annotations.get('distance'):
                if isinstance(distance, float):
                    # Format de la distance en fonction du système d'unités
                    unit_system = config['general']['unit_system']
                    if unit_system == 'meters':
                        distance_str = f'{distance:.2f} m'
                    elif unit_system == 'feet':
                        distance_str = f'{distance:.2f} ft'
                    elif unit_system == 'steps':
                        distance_str = f'{distance:.2f} steps'
                    else:
                        distance_str = f'{distance:.2f} m'  # Par défaut en mètres
                elif distance == 'too_close':
                    distance_str = translations.get('too_close', 'Trop proche')
                elif distance == 'too_far':
                    distance_str = translations.get('too_far', 'Hors de portée')
                else:
                    distance_str = translations.get('unknown_distance', 'Distance inconnue')
                label_lines.append(distance_str)

            # Dessiner la boîte englobante
            cv2.rectangle(image_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Procéder si des labels doivent être affichés
            if label_lines:
                # Calculer la hauteur totale du label
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                font_thickness = 1
                line_height = cv2.getTextSize('Tg', font, font_scale, font_thickness)[0][1] + 5  # Hauteur approximative de ligne

                total_label_height = line_height * len(label_lines)

                # Position de départ pour les labels
                label_x = x1
                label_y = y1 - total_label_height - 10  # 10 pixels au-dessus de la boîte

                # Ajuster si label_y est hors de l'image
                if label_y < 0:
                    label_y = y1 + 10  # Placer en dessous de la boîte

                # Dessiner le rectangle de fond pour les labels
                max_label_width = max([cv2.getTextSize(line, font, font_scale, font_thickness)[0][0] for line in label_lines]) + 10
                cv2.rectangle(image_bgr, (label_x, label_y), (label_x + max_label_width, label_y + total_label_height), (0, 255, 0), -1)

                # Ajouter chaque ligne de texte
                for i, line in enumerate(label_lines):
                    text_x = label_x + 5  # Padding à l'intérieur du rectangle
                    text_y = label_y + (i + 1) * line_height - 5  # Ajuster pour la ligne de base
                    cv2.putText(image_bgr, line, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness)

    if display_in_notebook:
        # Convertir l'image en RGB pour l'affichage avec matplotlib
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        # Afficher l'image annotée dans le notebook
        plt.figure(figsize=(10, 8))
        plt.imshow(image_rgb)
        plt.axis('off')
        plt.show()
    else:
        # Retourner le frame annoté pour affichage avec cv2.imshow
        return image_bgr

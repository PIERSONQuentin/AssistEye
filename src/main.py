import cv2
from AssistEye.detection import objectDetection, textDetection
from AssistEye.detection import depthEstimation
from AssistEye.translation import translation
from AssistEye.voiceAssistant import voiceAssistant
from AssistEye.visualization import visualization


##############################################################################################################
# Fonction principale du programme du projet AssistEye.
# Cette fonction initialise la webcam, capture une image, configure la carte de profondeur, effectue la détection d'objets,
# écoute une commande vocale et y répond.
##############################################################################################################
def main():
    # Variables globales
    best_text = ""

    # Initialiser la webcam.
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open the webcam")
        return

    try:
        while True:
            # Capturer une image de la webcam.
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to capture an image from the webcam")
                break

            # Configurer la carte de profondeur de l'image capturée.
            depth_map_normalized, processed_image = depthEstimation.configure_depth_map(frame, depthEstimation, display_mode="rgb")

            # Effectuer la détection d'objets dans l'image capturée.
            results = objectDetection.detect(frame)

            # Traiter les résultats pour obtenir le nombre d'objets, les distances et les positions
            object_counts, distances, positions = objectDetection.process_results(
                results, depth_map_normalized, return_positions=True
            )

            # Extraire les régions contenant les objets détectés
            cropped_regions = objectDetection.crop_objects(frame, positions)

            # Parcourir les régions recadrées et effectuer la détection de texte
            for class_name, regions in cropped_regions.items():
                for region in regions:
                    # Effectuer la détection de texte sur la région
                    text_results = textDetection.detect(region)
                    # Traiter les résultats pour obtenir le meilleur texte détecté
                    best_text = textDetection.process_results(text_results)

            # Ecouter une commande vocale et y répondre.
            command = voiceAssistant.listen()
            if command:
                voiceAssistant.process_command(command, object_counts, distances, best_text)

    except KeyboardInterrupt:
        print("\nUser interruption. Closing the program.")
    finally:
        cap.release()

# Entry point of the script.
if __name__ == "__main__":
    main()
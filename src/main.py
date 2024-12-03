import cv2
from AssistEye.detection import objectDetection
from AssistEye.depth import depth
from AssistEye.translation import translation
from AssistEye.voiceAssistant import voiceAssistant
from AssistEye.visualization import visualization

# Main function to run the AssistEye application POC.
def main():
    # Initialize the webcam.
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open the webcam")
        return

    try:
        while True:
            # Capture a frame from the webcam.
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to capture an image from the webcam")
                break

            # Configure the depth map and process the image.
            depth_map_normalized, processed_image = depth.configure_depth_map(frame, depth, display_mode="rgb")

            # Perform object detection on the captured frame.
            results = objectDetection.detect(frame)
            object_counts, distances = objectDetection.process_results(results, depth_map_normalized)

            # Listen for a voice command and process it.
            command = voiceAssistant.listen()
            if command:
                voiceAssistant.process_command(command, object_counts, distances)

    except KeyboardInterrupt:
        print("\nUser interruption. Closing the program.")
    finally:
        cap.release()

# Entry point of the script.
if __name__ == "__main__":
    main()
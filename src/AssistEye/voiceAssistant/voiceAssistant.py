"""
Voice Assistant Module

This module provides functionalities for speech synthesis and recognition.

Available functions:
- respond(text): Respond with speech synthesis.
- listen(): Listen and recognize a voice command.
- process_command(command, object_counts, distances): Process a voice command.
"""

import pyttsx3
import speech_recognition as sr

# Initialize the voice assistant components
engine = pyttsx3.init()
recognizer = sr.Recognizer()
translator = None  # This will be set with the initialize function

def voiceAssistant_init(translator_instance):
    """
    Initialize the voice assistant with speech synthesis and recognition.

    Args:
        translator_instance (Translation): Instance of the translator for responses.
    """
    global translator
    translator = translator_instance

def respond(text):
    """
    Respond with speech synthesis.

    Args:
        text (str): The text to speak.
    """
    print(f"IA : {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """
    Listen and recognize a voice command.

    Returns:
        str: The recognized voice command.
    """
    with sr.Microphone() as source:
        print("Écoute...")
        try:
            audio = recognizer.listen(source, timeout=3)
            return recognizer.recognize_google(audio, language="fr-FR").lower()
        except sr.UnknownValueError:
            print("Je n'ai pas compris.")
        except sr.RequestError as e:
            print(f"Erreur du service de reconnaissance vocale : {e}")
        except sr.WaitTimeoutError:
            pass
    return None

def process_command(command, object_counts, distances):
    """
    Process a voice command.

    Args:
        command (str): The recognized voice command.
        object_counts (dict): Dictionary of detected objects and their counts.
        distances (dict): Dictionary of detected objects and their distances.
    """
    translated_counts = {translator.translate_label(k): v for k, v in object_counts.items()}
    translated_distances = {translator.translate_label(k): v for k, v in distances.items()}

    for obj_type in translated_counts:
        if obj_type in command:
            if "combien" in command:
                count = translated_counts.get(obj_type, 0)
                if count:
                    response = translator.get_response("count_objects", count=count, object=obj_type)
                else:
                    response = translator.get_response("no_objects", object=obj_type)
                respond(response)
                return

            if "proche" in command:
                if obj_type in translated_distances:
                    closest_distance = min(translated_distances[obj_type])
                    response = translator.get_response("closest_object", object=obj_type, distance=round(closest_distance, 2))
                else:
                    response = translator.get_response("no_objects", object=obj_type)
                respond(response)
                return

    respond(translator.get_response("unknown_command"))
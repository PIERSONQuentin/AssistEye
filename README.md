# Project Architecture

```
├── config 
│   ├── config.yaml 
├── notebooks 
│   ├── example_integration.ipynb 
├── src 
│   ├── AssistEye 
│   │   ├── __init__.py 
│   │   ├── api
│   │   │   ├── __init__.py 
│   │   │   ├── api.py 
│   │   ├── config
│   │   │   ├── __init__.py 
│   │   │   ├── config.py 
│   │   ├── debug
│   │   │   ├── __init__.py 
│   │   │   ├── debug.py 
│   │   ├── depth
│   │   │   ├── __init__.py 
│   │   │   ├── depth.py 
│   │   ├── detection
│   │   │   ├── __init__.py 
│   │   │   ├── detection.py
│   │   ├── translation
│   │   │   ├── __init__.py 
│   │   │   ├── translation.py 
│   │   ├── visualization
│   │   │   ├── __init__.py 
│   │   │   ├── visualization.py
│   │   ├── voiceAssistant
│   │   │   ├── __init__.py 
│   │   │   ├── voiceAssistant.py 
│   ├── main.py
├── README.md 
```

### File Details

- **config**
  - `config.yaml`: Main configuration file for the project.

- **notebooks**
  - `example_integration.ipynb`: Example notebook demonstrating the integration of the AssistEye module.

- **src**
  - **AssistEye**
    - `__init__.py`: Initialization file for the AssistEye module.
    - `config.py`: Configuration management.
    - `depth.py`: Model and functions for depth estimation.
    - `detection.py`: Model and functions for object detection.
    - `translation.py`: Translation management.
    - `visualization.py`: Functions for visualizing results.
    - `voice.py`: Management of speech synthesis and recognition.
  - `main.py`: Main script to run the AssistEye application.

  ### Features of AssistEye Module

  The AssistEye module offers a range of functionalities designed to enhance user experience through advanced computer vision and natural language processing techniques. Below are the key features:

  - **Configuration Management**: Easily manage and customize settings using the `config.yaml` file.
  - **Depth Estimation**: Utilize the `depth.py` module to estimate the depth of objects in images.
  - **Object Detection**: Detect and identify objects within images using the `detection.py` module.
  - **Translation Services**: Translate text between different languages with the `translation.py` module.
  - **Visualization Tools**: Visualize data and results effectively using the `visualization.py` module.
  - **Voice Assistant**: Integrate speech synthesis and recognition capabilities with the `voice.py` module.

  These features collectively enable the AssistEye module to provide comprehensive support for various applications in computer vision and natural language processing.




  choses a mettres en place : 

- **Ajout de nouvelles commandes et fonctionnalités** : 
  - Commande pour que le voiceAssistant lise le texte détecté a l'utilisateur 
  - commandes pour changer les paramètres en modifiant dirrectement le fichier config.yaml
    - changer la langue 
  - changer la voix du voiceAssistant (utiliser autre chose que le TTS actuel)

- **Alternative à speech_recognition pour une plus grande variété de voix**

- **Personnalisation des commandes selon les préférences de l'utilisateur** : adapter les réponses en fonction de la rapidité et de la précision désirées par chaque utilisateur

- **Paramètres pour les unités de mesure** : proposer des options de changement entre mètres, pieds, pas ou autres unités (unité par défaut "pas")

- **Support multilingue** : ajout de l'anglais, par exemple (déjà fait mais a tester, modifier la gestion dans process_command pour prendre en charge les mots clés pour plusieurs langues)

- **Amélioration de la réponse vocale pour une meilleure contextualisation** : rendre les réponses plus naturelles et éviter les répétitions (par exemple, dire "À votre gauche" au lieu de "proche de vous").
  - Ajouter l'implémentation test de découpage de la zone de détection en zone pour avoir une meilleure contextualisation 



  ### Modules 

  Detection : 
  - objectDetection : Identifier les objets dans l'espace 

  - textDetection : Détecter le texte dans l'espace 

  - faceDetection : Identifier le visage des personnes dans l'espace 

  - sceneDetection : Identifier le type de scène (plage, forêt, ville) pour des applications de tri d'images ou d'assistance.

  - emotionDetection : Analyser les expressions faciales pour identifier des émotions comme la joie, la tristesse, la colère, etc.

  - anomalyDetection : Détecter des comportements ou objets anormaux dans une scène (sécurité, maintenance)

  - semanticSegmentation : Identifier les différents objets ou zones dans une image en assignant un label à chaque pixel.


---

### **Shared Methods**
1. **`initialization(model_name, device_name)`**  
   Initialise le modèle de détection avec le nom du modèle et l’appareil spécifié (par exemple, "CPU" ou "GPU"). Cela configure également tous les paramètres nécessaires au bon fonctionnement du modèle.

2. **`detect(frame)`**  
   Effectue la détection sur une image ou un cadre donné. Retourne les résultats de la détection, incluant les objets détectés, leurs coordonnées, et les scores de confiance.

3. **`process_results(results)`**  
   Traite les résultats de la détection pour extraire des informations utiles telles que les types d’objets, leurs quantités, ou leur position. Peut être étendu pour inclure des calculs personnalisés ou des filtrages.

4. **`run_inference(path, annotations)`**  
   Effectue une inférence sur un fichier image ou vidéo donné. Les annotations fournies permettent de spécifier des paramètres supplémentaires, tels que les types d’objets à détecter ou des zones d’intérêt dans l’image.

5. **`track_object(results)`** 
   Suit un ou plusieurs objets détectés dans des séquences d’images ou une vidéo. Retourne les positions et trajectoires des objets suivis au fil du temps.

6. **`batch_detect(frames)`**  
   Permet de traiter simultanément plusieurs images ou une séquence vidéo. Retourne une liste des résultats de détection pour chaque image ou frame.

7. **`export_results(results, format="json")`** 
   Exporte les résultats de la détection dans un format spécifié (par défaut, JSON). Peut également supporter d’autres formats comme CSV ou XML pour une meilleure intégration avec d'autres systèmes.

---
# AssistEye

AssistEye est un module complet destiné à fournir des fonctionnalités d'assistance visuelle et vocale. Il intègre la détection d'objets, l'estimation de profondeur, la détection de texte, la traduction multilingue, un assistant vocal interactif et une visualisation avancée. Ce projet a pour objectif d'aider les personnes malvoyantes et d'offrir une solution d'assistance intelligente dans divers contextes (domestique, professionnel, mobilité, etc.).

---
## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Architecture du projet](#architecture-du-projet)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
  - [Exécution de l'application](#exécution-de-lapplication)
  - [Utilisation de l'API](#utilisation-de-lapi)
  - [Exemple d'intégration Notebook](#exemple-dintégration-notebook)
- [Contribuer](#contribuer)

---

## Fonctionnalités

- **Détection d'objets**  
  Utilisation de modèles YOLO pour détecter des objets dans des images ou des vidéos avec un seuil de confiance configurable.

- **Estimation de profondeur**  
  Calcul de la carte de profondeur grâce au modèle MiDaS, permettant d'estimer la distance des objets dans la scène.

- **Détection de texte (OCR)**  
  Extraction de texte à partir d'images en utilisant Tesseract avec plusieurs prétraitements pour améliorer la précision.

- **Traduction et réponses multilingues**  
  Traduction des étiquettes d'objets et formulation de réponses dans différentes langues (ex. français et anglais).

- **Assistance vocale**  
  Interaction par commande vocale grâce à la reconnaissance (Speech Recognition) et à la synthèse vocale (pyttsx3). Le système est conçu pour être facilement extensible avec de nouvelles commandes via un mécanisme d'enregistrement basé sur des expressions régulières.

- **Visualisation et débogage**  
  Outils de visualisation pour afficher les résultats annotés (boîtes englobantes, distances, niveaux de confiance) sur les images ou les vidéos. Un module de débogage est également intégré pour faciliter le suivi des performances et des erreurs.

- **API REST**  
  Une API basée sur Flask permet d'exposer les fonctionnalités de détection d'objets et de texte via des endpoints HTTP, facilitant l'intégration dans d'autres applications.

---

## Architecture du projet

Le projet est organisé de manière modulaire pour faciliter sa maintenance et son évolutivité. Voici un aperçu de la structure des dossiers :

```plaintext
assist_eye/
├── __init__.py
├── api/
│   ├── __init__.py
│   └── api.py
├── config/
│   ├── __init__.py
│   └── config.py
├── detection/
│   ├── __init__.py
│   ├── objectDetection.py
│   ├── depthEstimation.py
│   └── textDetection.py
├── translation/
│   ├── __init__.py
│   └── translator.py
├── visualization/
│   ├── __init__.py
│   └── visualization.py
├── voiceAssistant/
│   ├── __init__.py
│   └── voiceAssistant.py
```

- **config/** : Charge et gère la configuration (fichier YAML) du module.
- **detection/** : Regroupe les modules de détection d'objets, d'estimation de profondeur et de détection de texte.
- **translation/** : Contient le module de traduction pour gérer la traduction des étiquettes et des réponses.
- **visualization/** : Fournit des fonctions pour l'annotation et l'affichage des résultats.
- **voice_assistant/** : Gère l'assistance vocale avec enregistrement et traitement des commandes.
- **api/** : Expose une API REST pour l'intégration externe.
- **utils/** : Regroupe des utilitaires, notamment pour la gestion des logs.

---

## Installation

### Prérequis

- **Python 3.7+**
- **Git** (pour cloner le dépôt)
- **Tesseract** installé et configuré pour l'OCR  
  (voir [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) pour l'installation)
- Les bibliothèques Python suivantes (liste non exhaustive) :
  - OpenCV
  - NumPy
  - PyTorch
  - Ultralytics (pour YOLO)
  - pytesseract
  - SpeechRecognition
  - pyttsx3
  - Flask
  - torchvision

### Installation des dépendances

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/PIERSONQuentin/AssistEye.git
   cd AssistEye
   ```

2. Installez les dépendances via pip :

   ```bash
   pip install -r requirements.txt
   ```

   *(Assurez-vous d'avoir créé et activé un environnement virtuel si nécessaire.)*

---

## Configuration

La configuration d'AssistEye se fait via un fichier YAML (par défaut `config/default.yaml`). Ce fichier permet de définir :

- Les modèles à utiliser pour la détection, l'estimation de profondeur et la détection de texte.
- Les paramètres généraux (langue, dispositif, seuils de confiance, système d'unités, etc.).
- Les paramètres spécifiques pour l'estimation de profondeur (facteur d'échelle, distances minimales et maximales).
- Les traductions pour les étiquettes et les réponses.

Vous pouvez modifier ce fichier ou créer un fichier personnalisé (par exemple, `config/custom.yaml`) et l'indiquer lors du lancement de l'application.

---

## Utilisation

### Exécution de l'application

Pour lancer l'application en mode démonstration via la webcam, exécutez :

```bash
python src/main.py
```

Ce script :

- Charge la configuration.
- Initialise les modules de détection, d'estimation de profondeur, de traduction et d'assistance vocale.
- Lance la capture vidéo depuis la webcam.
- Exécute la détection d'objets et l'estimation de profondeur en temps réel.
- Écoute et traite les commandes vocales.

### Utilisation de l'API

L'API REST est exposée via Flask et permet d'accéder aux fonctionnalités de détection d'objets et de texte. Pour démarrer l'API, exécutez :

```bash
python src/assist_eye/api/api.py
```

Les endpoints disponibles sont :

- **POST** `/detect_objects`  
  Reçoit une image et retourne les détections d'objets ainsi que leurs distances.

- **POST** `/detect_text`  
  Reçoit une image et retourne le texte détecté ainsi que les positions des zones de texte.

### Exemple d'intégration Notebook

Un notebook d'intégration complet est fourni dans le dossier `notebooks` (par exemple, `notebooks/example_integration.ipynb`). Ce notebook sert de documentation interactive pour apprendre à utiliser les différentes fonctionnalités d'AssistEye.

---

*AssistEye* est conçu pour être une solution modulaire, extensible et facile à maintenir. Nous espérons qu'il répondra à vos besoins et facilitera l'intégration d'une assistance visuelle et vocale dans vos projets.
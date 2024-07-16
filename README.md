# Tracker d'Exercice Workout AI

## Description
Le Tracker d'Exercice Workout AI est une application web qui aide les utilisateurs à suivre leurs exercices de fitness avec précision. L'application utilise un modèle de détection de pose basé sur YOLO pour surveiller et compter les exercices tels que les pompes des tractions et des squats en temps réel à l'aide d'une webcam.

## Fonctionnalités
- Surveillance en temps réel des exercices via une webcam
- Détection de pose et comptage d'exercices pour les pompes, tractions et squat
- Sélection dynamique des exercices avec réinitialisation automatique des flux vidéo

## Installation

### Prérequis
- Python 3.6+
- pip (gestionnaire de paquets Python)
- OpenCV
- Flask
- numpy
- ultralytics (YOLO)

### Étapes
1. Cloner le dépôt
    ```sh
    git clone https://github.com/Isaac64600/Workout_AI.git
    cd Workout_AI
    ```
2. Créer un environnement virtuel
    ```sh
    python -m venv venv
    ```
3. Activer l'environnement virtuel
    - Sur Windows :
        ```sh
        venv\Scripts\activate
        ```
    - Sur macOS/Linux :
        ```sh
        source venv/bin/activate
        ```
4. Installer les paquets requis
    ```sh
    pip install -r requirements.txt
    ```

## Utilisation
1. Exécuter l'application Flask
    ```sh
    python main.py
    ```
2. Ouvrir votre navigateur web et aller à `http://127.0.0.1:5000/`.

3. Sélectionner un exercice dans le menu déroulant. Le flux de la webcam affichera la détection de pose et le comptage des exercices.

## Structure des fichiers
- `main.py` : Fichier principal de l'application Flask qui configure les routes et gère les flux vidéo.
- `pull_up.py` : Script pour la détection et le comptage des tractions.
- `push_up.py` : Script pour la détection et le comptage des pompes.
- `squat.py` : Script pour la détection et le comptage des squats.
- `WorkOut_AI.ipynb` : Notebook Jupyter pour expérimenter avec le modèle de détection de pose.
- `yolov8n-pose.pt` : Fichier de poids du modèle YOLO pour la détection de pose.
- `templates/` : Répertoire pour les modèles HTML.
  - `workout.html` : Modèle HTML pour l'interface web.
- `static/` : Répertoire pour les fichiers statiques (CSS, JavaScript, vidéos).
  - `static/styles/style.css` : Fichier CSS pour le style de l'interface web.
  - `static/scripts/script.js` : Fichier JavaScript pour la gestion de la sélection des exercices et la mise à jour des flux vidéo.
  - `static/videos/` : Répertoire contenant des vidéos d'exercice d'exemple.
- `requirements.txt` : Fichier listant les paquets Python nécessaires.

## Aperçu du Code

### `app.py`
Contient l'application web Flask et les routes pour gérer différents flux vidéo. Il initialise et libère la capture vidéo, traite les frames et utilise un modèle YOLO pour détecter les poses et compter les exercices.

### `templates/workout.html`
Modèle HTML pour l'interface utilisateur. Il inclut un menu déroulant pour la sélection des exercices, des éléments vidéo pour la démonstration des exercices et le flux de la webcam, et des sections pour afficher le comptage des exercices.

### `static/scripts/script.js`
Fichier JavaScript qui gère la mise à jour dynamique des flux vidéo en fonction de l'exercice sélectionné. Il change la source des éléments vidéo et les recharge pour afficher le nouveau flux.

## Remerciements
- [YOLO](https://github.com/ultralytics/yolov5) pour le modèle de détection de pose
- [Flask](https://flask.palletsprojects.com/) pour le framework web
- [OpenCV](https://opencv.org/) pour le traitement vidéo

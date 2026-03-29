# 🌍 TalAIt - Plateforme de Traduction Sécurisée Fullstack

<!-- ![Status](https://img.shields.io/badge/Status-Completed-success) -->
![Stack](https://img.shields.io/badge/Fullstack-Next.js%20%2B%20FastAPI-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED)

## 📋 Contexte du Projet
La start-up marocaine **TalAIt**, spécialisée dans l’e-commerce, prépare son expansion aux États-Unis. Ce projet répond au besoin urgent de sécuriser et d'automatiser les traductions pour deux équipes clés :
* **Marketing :** Traduction des fiches produits (FR 🇫🇷 ➔ EN 🇺🇸).
* **Service Client :** Traitement des tickets (EN 🇺🇸 ➔ FR 🇫🇷).

L'application est une solution interne sécurisée, accessible uniquement aux employés authentifiés, exploitant l'IA via l'API Hugging Face.

---

## 🏗 Architecture 3-Tiers

L'application repose sur une architecture moderne et modulaire :

1.  **Frontend (Client) :** Next.js 14 (React + TypeScript + Tailwind CSS). Interface réactive et sécurisée.
2.  **Backend (API) :** FastAPI (Python). Gestion de l'authentification (JWT), logique métier et proxy vers l'IA.
3.  **Base de Données :** PostgreSQL. Stockage des utilisateurs.
4.  **Service IA Externe :** Hugging Face Inference API.



---

## 🛠 Stack Technique

* **Frontend :** Next.js, TypeScript, TailwindCSS, Axios/Fetch.
* **Backend :** FastAPI, Pydantic, SQLAlchemy, Passlib (Bcrypt), Python-Jose (JWT), HTTPX.
* **Base de Données :** PostgreSQL 13.
* **IA Models (Helsinki-NLP) :**
    * `opus-mt-fr-en` (Français vers Anglais)
    * `opus-mt-en-fr` (Anglais vers Français)
* **DevOps :** Docker, Docker Compose.

---

## 🚀 Installation et Démarrage Rapide

### Prérequis
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et lancé.
* Une clé API Hugging Face (gratuite).

### 1. Cloner le projet
```bash
git clone [https://github.com/votre-username/talait-project.git](https://github.com/votre-username/talait-project.git)
cd talait-project
````

### 2\. Configuration (.env)

Créez un fichier `.env` à la racine du projet et copiez-y le contenu suivant.
⚠️ **Important :** Remplacez `votre_token_ici` par votre vraie clé Hugging Face.

```env
# Base de données
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=talait_db
DATABASE_URL=postgresql://user:password@db:5432/talait_db

# Sécurité Backend
SECRET_KEY=une_cle_secrete_tres_longue_et_aleatoire_pour_jwt
ALGORITHM=HS256

# API IA Externe
HF_API_TOKEN=votre_token_hugging_face_ici
```

### 3\. Lancer l'application (Docker)

L'orchestration est entièrement gérée par Docker Compose.

```bash
docker-compose up --build
```

*Patientez quelques minutes lors du premier lancement (téléchargement des images et installation des dépendances).*

  * **Frontend :** Accessible sur `http://localhost:3000`
  * **Backend (Docs Swagger) :** Accessible sur `http://localhost:8000/docs`
  * **Base de Données :** Port `5432`

-----

## 📖 Documentation de l'API

L'API est sécurisée. Seuls `/login` et `/register` sont publics.

| Méthode | Endpoint | Description | Auth Requise |
| :--- | :--- | :--- | :--- |
| `POST` | `/register` | Inscription (username, password). Hashage automatique. | ❌ Non |
| `POST` | `/login` | Connexion. Retourne un `access_token` (JWT). | ❌ Non |
| `POST` | `/translate` | Traduit un texte. Champs : `{text, direction}`. | ✅ Oui (Bearer Token) |

### Modèles IA utilisés

Le backend sélectionne dynamiquement le modèle selon la direction demandée :

  * **FR ➔ EN :** `Helsinki-NLP/opus-mt-fr-en`
  * **EN ➔ FR :** `Helsinki-NLP/opus-mt-en-fr`

-----

## ✅ Tests Unitaires

Pour tester la logique backend sans lancer Docker (nécessite Python installé localement).

1.  Créer un environnement virtuel et installer les dépendances :

    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # ou venv\Scripts\activate sur Windows
    pip install -r requirements.txt
    pip install pytest httpx
    ```

2.  Lancer les tests :

    ```bash
    pytest test_main.py
    ```

    *Ces tests utilisent une base de données SQLite en mémoire et simulent (Mock) l'API Hugging Face.*

-----

## 🔒 Sécurité & Limitations

  * **JWT :** Les tokens expirent après 30 minutes.
  * **Mots de passe :** Hashés avec Bcrypt avant stockage.
  * **IA Cold Start :** L'API Hugging Face peut retourner une erreur 503 lors de la première requête (chargement du modèle). L'application gère ce cas, mais un re-essai manuel peut être nécessaire après 30 secondes.
